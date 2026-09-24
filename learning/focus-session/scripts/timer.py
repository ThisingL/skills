"""Windows learning timer: a small UI and JSON commands for the optional Skill."""

import argparse
import json
import sys
import webbrowser
from pathlib import Path

sys.dont_write_bytecode = True

from focus_service import call_timer, runtime_directory, serve, start_timer
from reporting import demo_session, write_report


def build_parser():
    parser = argparse.ArgumentParser(description='单次学习提醒器；无持续倒计时，复盘可独立使用。')
    sub = parser.add_subparsers(dest='command')
    start = sub.add_parser('start', help='启动独立后台提醒器，默认不记录应用')
    start.add_argument('--min-minutes', type=float, default=3)
    start.add_argument('--max-minutes', type=float, default=5)
    start.add_argument('--rest-seconds', type=float, default=10)
    start.add_argument('--limit-minutes', type=float, help='可选整场时长，包含暂停和休息')
    start.add_argument('--record', action='store_true', help='记录本次前台应用名')
    start.add_argument('--titles', action='store_true', help='另外记录窗口标题，须与 --record 一起使用')
    start.add_argument('--silent', action='store_true', help='静音运行')
    start.add_argument('--runtime-dir', type=Path)
    for command, help_text in [('status', '查看当前状态'), ('pause', '暂停'),
                               ('resume', '继续并重新安排随机间隔'), ('defer', '跳过本次休息或延后提醒'),
                               ('stop', '结束并生成本地报告'), ('gui', '打开小窗口')]:
        sub.add_parser(command, help=help_text).add_argument('--runtime-dir', type=Path)
    demo = sub.add_parser('demo', help='用虚构数据生成报告，不启动采集或音频')
    demo.add_argument('--output', type=Path, default=runtime_directory() / 'reports' / 'demo.html')
    demo.add_argument('--open', action='store_true')
    worker = sub.add_parser('_serve')
    worker.add_argument('--runtime-dir', required=True, type=Path)
    worker.add_argument('--options', required=True)
    worker.add_argument('--nonce', required=True)
    return parser


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if stream is not None and hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command in (None, 'gui'):
            from focus_ui import run_gui
            run_gui(getattr(args, 'runtime_dir', None))
            return 0
        if args.command == '_serve':
            serve(json.loads(args.options), args.runtime_dir, args.nonce)
            return 0
        if args.command == 'demo':
            path = write_report(demo_session(), args.output)
            result = {'demo': True, 'report_path': str(path)}
            if args.open:
                webbrowser.open(path.as_uri())
        elif args.command == 'start':
            if args.titles and not args.record:
                parser.error('--titles 需要同时指定 --record。')
            result = start_timer(dict(interval_min=args.min_minutes * 60,
                                      interval_max=args.max_minutes * 60,
                                      rest_seconds=args.rest_seconds,
                                      total_seconds=None if args.limit_minutes is None else args.limit_minutes * 60,
                                      recording_enabled=args.record,
                                      title_recording_enabled=args.titles,
                                      silent=args.silent), args.runtime_dir)
        else:
            result = call_timer(args.command, args.runtime_dir)
        print(json.dumps(result, ensure_ascii=True))
        return 0
    except (ValueError, OSError) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=True))
        return 1


if __name__ == '__main__':
    sys.exit(main())
