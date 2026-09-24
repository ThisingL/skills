"""Standalone, offline report rendering."""

import json
from pathlib import Path


APP_NAMES = {
    'msedge.exe': 'Microsoft Edge',
    'chrome.exe': 'Google Chrome',
    'code.exe': 'Visual Studio Code',
    'windowsterminal.exe': 'Windows Terminal',
    'qq.exe': 'QQ',
    'explorer.exe': '文件资源管理器',
}


def summarize_session(data):
    """Bound the conversation payload; titles, raw segments and idle signals stay out."""
    recording = bool(data.get('recording_enabled'))
    summary = dict(duration_seconds=data['duration_seconds'], activity_seconds=0,
                   rest_seconds=0, paused_seconds=0, unobserved_seconds=0,
                   recording_enabled=recording,
                   title_recording_enabled=bool(recording and data.get('title_recording_enabled')),
                   apps=[], remaining_apps=dict(count=0, seconds=0))
    state_fields = dict(focus='activity_seconds', rest='rest_seconds',
                        paused='paused_seconds', unobserved='unobserved_seconds')
    apps = {}
    for segment in data['segments']:
        seconds = max(0, segment['end'] - segment['start'])
        field = state_fields.get(segment['state'])
        if field:
            summary[field] += seconds
        if recording and segment['state'] == 'focus' and seconds:
            process = segment.get('app') or None
            key = process.casefold() if process else None
            if key not in apps:
                apps[key] = dict(process=process,
                                 name=APP_NAMES.get(key, process or '未识别应用'), seconds=0)
            apps[key]['seconds'] += seconds
    for field in state_fields.values():
        summary[field] = round(summary[field], 6)
    ranked = sorted(apps.values(), key=lambda app: app['seconds'], reverse=True)
    for app in ranked:
        app['seconds'] = round(app['seconds'], 6)
    summary['apps'] = ranked[:8]
    summary['remaining_apps'] = dict(count=len(ranked[8:]),
                                     seconds=round(sum(app['seconds'] for app in ranked[8:]), 6))
    return summary


def encode_session(data):
    return (json.dumps(data, ensure_ascii=False, allow_nan=False)
            .replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
            .replace('\u2028', '\\u2028').replace('\u2029', '\\u2029'))


def write_report(data, destination, template=None):
    template = Path(template) if template else Path(__file__).resolve().parents[1] / 'assets' / 'report_template.html'
    content = template.read_text(encoding='utf-8')
    if content.count('__SESSION_JSON__') != 1:
        raise ValueError('报告模板缺少唯一的数据占位符。')
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content.replace('__SESSION_JSON__', encode_session(data)), encoding='utf-8')
    return destination.resolve()


def demo_session():
    """Fictional data only, never a read of the user's desktop."""
    activities = [(12, 'focus', '浏览器 / PDF', 'RAG 方法与检索流程'),
                  (10, 'focus', 'VS Code', '检索参数实验'),
                  (4, 'focus', '浏览器', '信息流首页'),
                  (8, 'focus', 'AI 对话', '讨论实验现象'),
                  (4, 'focus', '浏览器', '视频详情页'),
                  (4, 'rest', None, ''),
                  (8, 'focus', '浏览器 / PDF', '对照资料'),
                  (8, 'focus', 'VS Code', '验证参数'),
                  (2, 'paused', None, '')]
    cursor, segments = 0, []
    for minutes, state, app, title in activities:
        end = cursor + minutes * 60
        segments.append(dict(start=cursor, end=end, state=state, app=app,
                             title=title, idle_seconds=None))
        cursor = end
    return dict(schema_version=1, session_id='demo', demo=True,
                started_at='2026-09-22T14:00:00+08:00', ended_at='2026-09-22T15:00:00+08:00',
                duration_seconds=cursor, recording_enabled=True,
                title_recording_enabled=True, end_reason='manual', segments=segments)
