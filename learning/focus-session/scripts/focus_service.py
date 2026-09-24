"""A small authenticated loopback service so UI and Skill share one timer."""

import contextlib
import hashlib
import hmac
import http.client
import json
import os
import secrets
import subprocess
import sys
import tempfile
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from focus_core import Session
from reporting import summarize_session, write_report


class TimerRuntime:
    def __init__(self, session, activity, sound, report_dir):
        self.session, self.activity, self.sound = session, activity, sound
        self.report_dir = Path(report_dir)
        self.report_path = None
        self.summary = None
        self.audio_warning = ''
        self.next_sample = 0
        self.observation = None
        self._begun = False

    def begin(self):
        """Announce a newly ready service, without constructor side effects."""
        if not self._begun and self.session.state == 'focus':
            self._begun = True
            self._play('start_focus')

    def _play(self, event):
        if self.sound(event) is False:
            self.audio_warning = '声音播放失败，请检查输出设备；学习状态仍会正常更新。'

    def _stop_audio(self):
        if getattr(self.sound, 'stop', lambda: True)() is False:
            self.audio_warning = '声音停止失败，请检查输出设备；学习状态仍会正常更新。'

    def tick(self):
        if self.session.state == 'ended':
            self._finish()
            return
        available = self.activity.desktop_available() if self.session.state != 'paused' else True
        events = self.session.advance(observation=self.observation, desktop_available=available)
        now = self.session.last
        if self.session.state != 'focus' or not available:
            self.observation = None
            self.next_sample = 0
        elif self.session.recording_enabled and now >= self.next_sample:
            self.observation = self.activity.sample(include_title=self.session.title_recording_enabled)
            self.next_sample = now + 2
        self.session.observation = self.observation
        for event in events:
            if event in ('rest_start', 'rest_end'):
                self._play(event)
            elif event == 'auto_pause':
                self._stop_audio()
        if self.session.state == 'ended':
            self._finish()

    def _finish(self):
        if self.report_path is None:
            data = self.session.stop()
            self.report_path = str(write_report(data, self.report_dir / (data['session_id'] + '.html')))
            self.summary = summarize_session(data)
            self._play('session_end')

    def status(self):
        return dict(state=self.session.state, session_id=self.session.session_id,
                    elapsed_seconds=round(self.session.last, 2),
                    recording_enabled=self.session.recording_enabled,
                    title_recording_enabled=self.session.title_recording_enabled,
                    pause_reason=self.session.pause_reason,
                    report_path=self.report_path, audio_warning=self.audio_warning, summary=self.summary)

    def command(self, action):
        self.tick()
        if action == 'status':
            return self.status()
        if action not in ('pause', 'resume', 'defer', 'stop'):
            raise ValueError('未知的计时器操作。')
        if action == 'resume' and not self.activity.desktop_available():
            raise ValueError('桌面仍不可用，请解锁后再继续。')
        previous_state = self.session.state
        if action == 'stop':
            self.session.stop()
            self._finish()
        else:
            getattr(self.session, action)()
            self.observation = None
            self.next_sample = 0
            if self.session.state == 'ended':
                self._finish()
            elif self.session.state == 'paused' and previous_state != 'paused':
                self._stop_audio()
            elif action == 'resume' and previous_state == 'paused' and self.session.state == 'focus':
                self._play('resume_focus')
            elif action == 'defer' and previous_state == 'rest' and self.session.state == 'focus':
                self._play('rest_end')
        return self.status()


def make_server(runtime, token):
    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup()
            self.connection.settimeout(1)

        def log_message(self, *args):
            pass  # Never log headers, tokens, or window data.

        def do_GET(self):
            self._respond(False)

        def do_POST(self):
            self._respond(True)

        def _respond(self, mutation):
            if not hmac.compare_digest(self.headers.get('X-Focus-Token', ''), token):
                code, result = 403, {'error': '无效的本地工具凭据。'}
            elif self.path not in ('/status', '/pause', '/resume', '/defer', '/stop'):
                code, result = 404, {'error': '未知操作。'}
            elif (self.path == '/status') == mutation:
                code, result = 405, {'error': '该操作不支持此 HTTP 方法。'}
            else:
                try:
                    code, result = 200, runtime.command(self.path[1:])
                except ValueError as error:
                    code, result = 409, {'error': str(error)}
                except OSError:
                    code, result = 500, {'error': '本地报告写入失败，请检查临时目录。'}
            body = json.dumps(result, ensure_ascii=True).encode('utf-8')
            self.send_response(code)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)

    server = HTTPServer(('127.0.0.1', 0), Handler)
    server.timeout = 0.25
    return server


def runtime_directory():
    project = str(Path(__file__).resolve().parent)
    suffix = hashlib.sha256(project.encode('utf-8')).hexdigest()[:12]
    return Path(tempfile.gettempdir()) / ('random-reminder-' + suffix)


def _save_descriptor(directory, data):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    pending = directory / 'active.pending'
    pending.write_text(json.dumps(data), encoding='utf-8')
    os.replace(str(pending), str(directory / 'active.json'))


def _read_descriptor(directory):
    try:
        return json.loads((Path(directory) / 'active.json').read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def call_timer(action='status', directory=None):
    directory = _absolute_directory(directory)
    descriptor = _read_descriptor(directory)
    if not descriptor:
        if action == 'status':
            return {'state': 'idle'}
        raise ValueError('当前没有正在运行的计时器。')
    if descriptor.get('state') in ('ended', 'error'):
        if action in ('status', 'stop'):
            return {k: v for k, v in descriptor.items() if k not in ('token', 'port', 'pid', 'nonce')}
        raise ValueError('本次计时已结束，请开始一次新学习。')
    missing_worker = '计时器进程已退出，本次未完成的记录无法恢复；可以开始新的一次。'
    if not descriptor.get('port') or not descriptor.get('token'):
        if descriptor.get('pid') and not _pid_running(descriptor['pid']):
            if action in ('status', 'stop'):
                return {'state': 'error', 'error': missing_worker}
            raise ValueError(missing_worker)
        raise ValueError('计时器进程尚未就绪，请稍后重试。')
    connection = http.client.HTTPConnection('127.0.0.1', descriptor['port'], timeout=2)
    try:
        connection.request('GET' if action == 'status' else 'POST', '/' + action,
                           headers={'X-Focus-Token': descriptor['token']})
        response = connection.getresponse()
        result = json.loads(response.read())
        if response.status != 200:
            raise ValueError(result.get('error', '计时器操作失败。'))
        return result
    except (OSError, http.client.HTTPException, ValueError, KeyError) as error:
        if isinstance(error, ValueError) and str(error).startswith(('桌面', '本地')):
            raise
        if descriptor.get('pid') and not _pid_running(descriptor['pid']):
            if action in ('status', 'stop'):
                return {'state': 'error', 'error': missing_worker}
            raise ValueError(missing_worker) from error
        raise ValueError('无法连接计时器：' + str(error))
    finally:
        connection.close()


@contextlib.contextmanager
def _start_lock(directory):
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / 'start.lock').open('a+b') as handle:
        if handle.tell() == 0:
            handle.write(b'0')
            handle.flush()
        handle.seek(0)
        if os.name == 'nt':
            import msvcrt
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == 'nt':
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle, fcntl.LOCK_UN)


def _pid_running(pid):
    if not isinstance(pid, int) or pid <= 0:
        return False
    if os.name == 'nt':
        import ctypes
        from ctypes import wintypes
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel.OpenProcess.restype = wintypes.HANDLE
        kernel.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        kernel.WaitForSingleObject.restype = wintypes.DWORD
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        process = kernel.OpenProcess(0x00100000, False, pid)
        if not process:
            return ctypes.get_last_error() == 5  # Access denied: don't risk a second timer.
        try:
            return kernel.WaitForSingleObject(process, 0) == 258
        finally:
            kernel.CloseHandle(process)
    try:
        os.kill(pid, 0)  # POSIX probe only. This must never be used on Windows.
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def _absolute_directory(directory):
    return Path(os.path.abspath(directory if directory is not None else runtime_directory()))


def _cancel_start(process, directory, nonce):
    """Never release the startup lock with an untracked worker still alive."""
    try:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=2)
    except (OSError, subprocess.TimeoutExpired) as error:
        latest = _read_descriptor(directory)
        if latest.get('nonce') != nonce or latest.get('state') in ('ended', 'error'):
            _save_descriptor(directory, dict(state='starting', pid=process.pid, nonce=nonce))
        raise ValueError('启动失败，后台进程未能退出；已保留进程信息以防重复启动。') from error
    latest = _read_descriptor(directory)
    if latest.get('nonce') == nonce and latest.get('state') not in ('ended', 'error'):
        _save_descriptor(directory, dict(state='error', error='启动失败，后台进程已退出。', nonce=nonce))


def start_timer(options, directory=None):
    directory = _absolute_directory(directory)
    # Validate before launching any process, without desktop or audio access.
    Session(**{key: value for key, value in options.items() if key != 'silent'})
    with _start_lock(directory):
        descriptor = _read_descriptor(directory)
        if descriptor.get('state') not in (None, 'ended', 'error'):
            try:
                status = call_timer('status', directory)
                if status.get('state') in ('focus', 'rest', 'paused'):
                    status['already_running'] = True
                    return status
                raise ValueError('已有会话不再运行。')
            except ValueError:
                if _pid_running(descriptor.get('pid')):
                    raise ValueError('已有计时器进程，但暂时无法连接；请稍后重试。')
        nonce = secrets.token_hex(16)
        command = [sys.executable, str(Path(__file__).with_name('timer.py')), '_serve',
                   '--runtime-dir', str(directory), '--nonce', nonce,
                   '--options', json.dumps(options)]
        kwargs = {'creationflags': subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {'start_new_session': True}
        with (directory / 'startup.log').open('w', encoding='utf-8') as log:
            process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=log, stderr=log,
                                       cwd=str(Path(__file__).resolve().parent), **kwargs)
        try:
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline:
                latest = _read_descriptor(directory)
                if latest.get('nonce') == nonce:
                    if latest.get('state') == 'error':
                        raise ValueError(latest.get('error', '计时器启动失败。'))
                    return call_timer('status', directory)
                if process.poll() is not None:
                    break
                time.sleep(0.05)
            raise ValueError('计时器尚未就绪；诊断日志：' + str(directory / 'startup.log'))
        except BaseException:
            _cancel_start(process, directory, nonce)
            raise


def serve(options, directory, nonce):
    from sounds import AudioPlayer
    from windows_activity import WindowsActivity
    directory = _absolute_directory(directory)
    audio = None
    try:
        config = dict(options)
        silent = config.pop('silent', False)
        audio = AudioPlayer(silent=silent)
        runtime = TimerRuntime(Session(**config), WindowsActivity(), audio, directory / 'reports')
        token = secrets.token_hex(32)
        with make_server(runtime, token) as server:
            _save_descriptor(directory, dict(state='running', port=server.server_port,
                                             token=token, pid=os.getpid(), nonce=nonce))
            runtime.begin()
            while runtime.session.state != 'ended':
                runtime.tick()
                if runtime.session.state != 'ended':
                    server.handle_request()
            result = runtime.status()
            result['nonce'] = nonce
            _save_descriptor(directory, result)
        # End requests and the terminal descriptor are already delivered. Only
        # the detached worker waits here so its final cue is not cut short.
        audio.finish()
    except Exception as error:
        if audio is not None:
            audio.stop()
        _save_descriptor(directory, dict(state='error', error=str(error), nonce=nonce))
        raise
