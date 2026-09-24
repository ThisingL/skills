"""Original audio cues, decoded to PCM WAV for native asynchronous playback."""

import sys
import time
import wave
from pathlib import Path


AUDIO_FILES = {
    'start_focus': 'long_rest_start.wav',
    'resume_focus': 'short_rest_end.wav',
    'rest_start': 'short_rest_start.wav',
    'rest_end': 'short_rest_end.wav',
    'session_end': 'long_rest_start.wav',
}


class AudioPlayer:
    def __init__(self, silent=False, audio_dir=None, backend=None,
                 clock=time.monotonic, sleep=time.sleep):
        self.silent = silent
        self.audio_dir = Path(audio_dir) if audio_dir else Path(__file__).resolve().parents[1] / 'assets' / 'audio'
        self.backend = backend
        self.clock, self.sleep = clock, sleep
        self.active = False
        self.ends_at = 0

    def __call__(self, event):
        if self.silent:
            return True
        name = AUDIO_FILES.get(event)
        if name is None:
            return False
        try:
            path = self.audio_dir / name
            with wave.open(str(path), 'rb') as recording:
                duration = recording.getnframes() / recording.getframerate()
            if self.backend is None:
                if not sys.platform.startswith('win'):
                    return False
                import winsound
                self.backend = winsound
            if not self.stop():
                return False
            flags = self.backend.SND_FILENAME | self.backend.SND_ASYNC | self.backend.SND_NODEFAULT
            self.backend.PlaySound(str(path), flags)
            self.active = True
            self.ends_at = self.clock() + duration + 0.1
            return True
        except (OSError, RuntimeError, ImportError, EOFError, wave.Error):
            # Surface failure instead of silently replacing the user's chosen sound.
            return False

    def stop(self):
        if not self.active:
            return True
        self.active = False
        self.ends_at = 0
        try:
            self.backend.PlaySound(None, 0)
            return True
        except (OSError, RuntimeError):
            return False

    def finish(self):
        """Call only after replying to stop and publishing the final session state."""
        if self.active:
            remaining = max(0, self.ends_at - self.clock())
            if remaining:
                self.sleep(remaining)
            self.stop()
