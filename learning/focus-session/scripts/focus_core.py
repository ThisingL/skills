"""Clock-driven state and per-session activity records; no OS or UI side effects."""

import math
import random
import time
import uuid
from datetime import datetime, timedelta


class Session:
    """One independent session. Inactivity is a signal, never a focus verdict."""

    MAX_SAMPLE_GAP = 15

    def __init__(self, interval_min=180, interval_max=300, rest_seconds=10,
                 total_seconds=None, recording_enabled=False,
                 title_recording_enabled=False, clock=time.monotonic,
                 random_interval=random.uniform, started_at=None):
        for value in (interval_min, interval_max, rest_seconds):
            if not math.isfinite(value) or value <= 0:
                raise ValueError('提醒间隔和休息时长必须是有限的正数。')
        if interval_min > interval_max:
            raise ValueError('最小提醒间隔不能大于最大间隔。')
        if total_seconds is not None and (not math.isfinite(total_seconds) or total_seconds <= 0):
            raise ValueError('结束时长必须是有限的正数，或留空。')
        self.interval_min, self.interval_max = interval_min, interval_max
        self.rest_seconds, self.total_seconds = rest_seconds, total_seconds
        self.recording_enabled = bool(recording_enabled)
        self.title_recording_enabled = bool(recording_enabled and title_recording_enabled)
        self.clock, self.random_interval = clock, random_interval
        self.origin = clock()
        self.started_at = started_at or datetime.now().astimezone()
        self.session_id = uuid.uuid4().hex
        self.state = 'focus'
        self.last = 0.0
        self.deadline = self._next_interval()
        self.observation = None
        self.segments = []
        self.end_reason = None
        self.pause_reason = ''

    def _next_interval(self):
        return self.random_interval(self.interval_min, self.interval_max)

    def _record(self, start, end, state):
        if end <= start:
            return
        observation = self.observation if state == 'focus' and self.recording_enabled else None
        observation = observation or {}
        segment = dict(start=round(start, 6), end=round(end, 6), state=state,
                       app=observation.get('app'),
                       title=observation.get('title', '') if self.title_recording_enabled else '',
                       idle_seconds=observation.get('idle_seconds'))
        previous = self.segments[-1] if self.segments else None
        if previous and all(previous[k] == segment[k] for k in ('state', 'app', 'title')):
            previous['end'] = segment['end']
            values = [v for v in (previous['idle_seconds'], segment['idle_seconds']) if v is not None]
            previous['idle_seconds'] = max(values) if values else None
        else:
            self.segments.append(segment)

    def advance(self, observation=None, desktop_available=True):
        if self.state == 'ended':
            return []
        target = max(self.last, self.clock() - self.origin)
        gap = target - self.last > self.MAX_SAMPLE_GAP
        if self.total_seconds is not None:
            target = min(target, self.total_seconds)
        events = []
        if self.state != 'paused' and (gap or not desktop_available):
            # We cannot reconstruct activity during a suspended process or inaccessible desktop.
            self._record(self.last, target, 'unobserved')
            self.state = 'paused'
            self.deadline = None
            self.observation = None
            self.pause_reason = '系统暂停或采样中断' if gap else '锁屏或桌面不可用'
            events.append('auto_pause')
        elif self.state == 'paused':
            self._record(self.last, target, 'paused')
        else:
            cursor = self.last
            while cursor < target:
                boundary = min(target, self.deadline)
                self._record(cursor, boundary, self.state)
                cursor = boundary
                # A session limit takes precedence over a reminder at the same instant.
                if self.total_seconds is not None and cursor >= self.total_seconds:
                    break
                if cursor >= self.deadline:
                    if self.state == 'focus':
                        self.state = 'rest'
                        self.deadline = cursor + self.rest_seconds
                        events.append('rest_start')
                    else:
                        self.state = 'focus'
                        self.deadline = cursor + self._next_interval()
                        events.append('rest_end')
                    self.observation = None
        self.last = target
        if self.total_seconds is not None and target >= self.total_seconds:
            self.state = 'ended'
            self.end_reason = 'time_limit'
            self.observation = None
            return ['session_end']
        self.observation = observation if self.state == 'focus' and self.recording_enabled else None
        return events

    def pause(self):
        self.advance()
        if self.state != 'ended':
            self.state = 'paused'
            self.pause_reason = '手动暂停'
            self.deadline = None
            self.observation = None

    def resume(self):
        self.advance()
        if self.state == 'paused':
            self.state = 'focus'
            self.pause_reason = ''
            self.deadline = self.last + self._next_interval()

    def defer(self):
        """Skip this micro-break, or reschedule the next reminder, without a penalty."""
        self.advance()
        if self.state in ('focus', 'rest'):
            self.state = 'focus'
            self.deadline = self.last + self._next_interval()

    def stop(self, reason='manual'):
        if self.state != 'ended':
            self.advance()
            if self.state != 'ended':
                self.state = 'ended'
                self.end_reason = reason
        return dict(schema_version=1, session_id=self.session_id,
                    started_at=self.started_at.isoformat(),
                    ended_at=(self.started_at + timedelta(seconds=self.last)).isoformat(),
                    duration_seconds=round(self.last, 6),
                    recording_enabled=self.recording_enabled,
                    title_recording_enabled=self.title_recording_enabled,
                    end_reason=self.end_reason,
                    segments=[dict(segment) for segment in self.segments])
