"""Optional Windows activity metadata; importing this module collects nothing.

Only call ``sample`` after the user opts into application recording. Window
titles require a separate opt-in. Idle time describes input inactivity, not
whether a person is away or concentrating.
"""

import ctypes
from ctypes import wintypes
import ntpath
import sys


class _LastInputInfo(ctypes.Structure):
    _fields_ = [('cbSize', wintypes.UINT), ('dwTime', wintypes.DWORD)]


class WindowsActivity:
    def __init__(self):
        self._windows = sys.platform == 'win32'
        self._user32 = None
        self._kernel32 = None

    def _load(self):
        if not self._windows:
            return False
        if self._user32 is not None:
            return True
        try:
            user32 = ctypes.WinDLL('user32', use_last_error=True)
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            # ctypes otherwise assumes a 32-bit int result, truncating handles.
            signatures = (
                (user32.OpenInputDesktop, [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD], wintypes.HANDLE),
                (user32.GetUserObjectInformationW,
                 [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD,
                  ctypes.POINTER(wintypes.DWORD)], wintypes.BOOL),
                (user32.CloseDesktop, [wintypes.HANDLE], wintypes.BOOL),
                (user32.GetForegroundWindow, [], wintypes.HWND),
                (user32.GetWindowThreadProcessId,
                 [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)], wintypes.DWORD),
                (user32.GetWindowTextLengthW, [wintypes.HWND], ctypes.c_int),
                (user32.GetWindowTextW, [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int], ctypes.c_int),
                (user32.GetLastInputInfo, [ctypes.POINTER(_LastInputInfo)], wintypes.BOOL),
                (kernel32.OpenProcess, [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD], wintypes.HANDLE),
                (kernel32.QueryFullProcessImageNameW,
                 [wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR,
                  ctypes.POINTER(wintypes.DWORD)], wintypes.BOOL),
                (kernel32.CloseHandle, [wintypes.HANDLE], wintypes.BOOL),
                (kernel32.GetTickCount, [], wintypes.DWORD),
            )
            for function, arguments, result in signatures:
                function.argtypes = arguments
                function.restype = result
            self._user32, self._kernel32 = user32, kernel32
            return True
        except (OSError, AttributeError):
            return False

    def desktop_available(self):
        """Whether the input desktop is Default, avoiding secure desktops."""
        if not self._windows:
            return True
        if not self._load():
            return False
        desktop = None
        try:
            desktop = self._user32.OpenInputDesktop(0, False, 0x0001)  # DESKTOP_READOBJECTS
            if not desktop:
                return False
            name = ctypes.create_unicode_buffer(256)
            needed = wintypes.DWORD()
            if not self._user32.GetUserObjectInformationW(
                    desktop, 2, name, ctypes.sizeof(name), ctypes.byref(needed)):
                return False
            return name.value.casefold() == 'default'
        except (OSError, ValueError, ctypes.ArgumentError):
            return False
        finally:
            if desktop:
                try:
                    self._user32.CloseDesktop(desktop)
                except OSError:
                    pass

    def _app_name(self, window):
        process = None
        try:
            pid = wintypes.DWORD()
            if not self._user32.GetWindowThreadProcessId(window, ctypes.byref(pid)) or not pid.value:
                return None
            process = self._kernel32.OpenProcess(0x1000, False, pid.value)
            if not process:
                return None
            path = ctypes.create_unicode_buffer(32768)
            length = wintypes.DWORD(len(path))
            if self._kernel32.QueryFullProcessImageNameW(process, 0, path, ctypes.byref(length)):
                return ntpath.basename(path.value) or None
        except (OSError, ValueError, ctypes.ArgumentError):
            pass
        finally:
            if process:
                try:
                    self._kernel32.CloseHandle(process)
                except OSError:
                    pass
        return None

    def _window_title(self, window):
        try:
            length = self._user32.GetWindowTextLengthW(window)
            if length > 0:
                title = ctypes.create_unicode_buffer(min(length + 1, 32768))
                if self._user32.GetWindowTextW(window, title, len(title)) > 0:
                    return title.value
        except (OSError, ValueError, ctypes.ArgumentError):
            pass
        return ''

    def _idle_seconds(self):
        try:
            last_input = _LastInputInfo()
            last_input.cbSize = ctypes.sizeof(last_input)
            if self._user32.GetLastInputInfo(ctypes.byref(last_input)):
                # Both counters use the low 32 bits and wrap after 49.7 days.
                return ((self._kernel32.GetTickCount() - last_input.dwTime) & 0xFFFFFFFF) / 1000.0
        except (OSError, ValueError, ctypes.ArgumentError):
            pass
        return None

    def sample(self, include_title=False):
        """Return one observation; unavailable fields stay explicitly unknown."""
        result = {'app': None, 'title': '', 'idle_seconds': None}
        if not self._windows or not self._load() or not self.desktop_available():
            return result
        result['idle_seconds'] = self._idle_seconds()
        try:
            window = self._user32.GetForegroundWindow()
            if window:
                result['app'] = self._app_name(window)
                if include_title:
                    result['title'] = self._window_title(window)
        except (OSError, ValueError, ctypes.ArgumentError):
            pass
        return result
