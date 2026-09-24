"""A quiet control window: state and actions, never a running countdown."""

import sys
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import messagebox, ttk

from focus_service import call_timer, start_timer


class FocusWindow:
    def __init__(self, root, directory=None):
        self.root, self.directory = root, directory
        self.active = False
        self.report_path = None
        self.state = 'idle'
        self.after_id = None
        root.title('留白 · 单次学习')
        root.geometry('560x550')
        root.minsize(490, 530)
        root.configure(bg='#f5f4ed')
        style = ttk.Style(root)
        style.theme_use('clam')
        style.configure('.', font=('Microsoft YaHei UI', 10), background='#f5f4ed')
        style.configure('TButton', padding=(12, 9))
        style.configure('TCheckbutton', padding=(0, 4))
        frame = ttk.Frame(root, padding=26)
        frame.pack(fill='both', expand=True)
        ttk.Label(frame, text='留一点空间，专心做眼前的事。', font=('Microsoft YaHei UI', 17)).pack(anchor='w')
        ttk.Label(frame, text='随机轻提醒 · 不显示倒计时 · 每次独立', foreground='#536b61').pack(anchor='w', pady=(7, 20))
        self.settings = ttk.Frame(frame)
        self.settings.pack(fill='x')
        self.values = {}
        for row, (key, label, default) in enumerate([
                ('min', '提醒间隔最短（分钟）', '3'), ('max', '提醒间隔最长（分钟）', '5'),
                ('rest', '微休息（秒）', '10'), ('limit', '整场时长（分钟，留空手动结束）', '')]):
            ttk.Label(self.settings, text=label).grid(row=row, column=0, sticky='w', pady=5)
            value = tk.StringVar(value=default)
            ttk.Entry(self.settings, textvariable=value, width=10).grid(row=row, column=1, sticky='e', padx=(15, 0))
            self.values[key] = value
        self.settings.columnconfigure(0, weight=1)
        self.record = tk.BooleanVar(value=False)
        self.titles = tk.BooleanVar(value=False)
        self.silent = tk.BooleanVar(value=False)
        self.record_check = ttk.Checkbutton(self.settings, text='记录本次前台应用（每 2 秒采样）', variable=self.record,
                                            command=self.update_titles)
        self.record_check.grid(row=4, column=0, columnspan=2, sticky='w', pady=(12, 0))
        self.title_check = ttk.Checkbutton(self.settings, text='另外记录窗口标题（可能含视频/文档名）', variable=self.titles)
        self.title_check.grid(row=5, column=0, columnspan=2, sticky='w')
        ttk.Checkbutton(self.settings, text='静音', variable=self.silent).grid(row=6, column=0, sticky='w')
        if not sys.platform.startswith('win'):
            self.record_check.state(['disabled'])
        self.update_titles()
        self.status_text = tk.StringVar(value='准备好了，就开始。')
        self.notice = tk.StringVar(value='只想复盘？直接在 Agent 中使用 $focus-session 即可。')
        ttk.Label(frame, textvariable=self.status_text, font=('Microsoft YaHei UI', 15)).pack(anchor='w', pady=(20, 8))
        ttk.Label(frame, textvariable=self.notice, wraplength=480, foreground='#536b61').pack(anchor='w')
        self.actions = ttk.Frame(frame)
        self.actions.pack(fill='x', pady=(18, 0))
        self.start_button = ttk.Button(self.actions, text='开始学习', command=self.start)
        self.start_button.pack(side='left')
        self.pause_button = ttk.Button(self.actions, text='暂停', command=self.pause_resume)
        self.defer_button = ttk.Button(self.actions, text='稍后提醒', command=lambda: self.control('defer'))
        self.stop_button = ttk.Button(self.actions, text='结束', command=lambda: self.control('stop'))
        self.report_button = ttk.Button(frame, text='查看本次时间轴', command=self.open_report)
        root.protocol('WM_DELETE_WINDOW', self.close)
        self.poll()

    def update_titles(self):
        if not self.record.get():
            self.titles.set(False)
            self.title_check.state(['disabled'])
        else:
            self.title_check.state(['!disabled'])

    def start(self):
        try:
            limit = self.values['limit'].get().strip()
            options = dict(interval_min=float(self.values['min'].get()) * 60,
                           interval_max=float(self.values['max'].get()) * 60,
                           rest_seconds=float(self.values['rest'].get()),
                           total_seconds=float(limit) * 60 if limit else None,
                           recording_enabled=self.record.get(), title_recording_enabled=self.titles.get(),
                           silent=self.silent.get())
            status = start_timer(options, self.directory)
            self.render(status)
        except (ValueError, OSError) as error:
            messagebox.showerror('还不能开始', str(error), parent=self.root)

    def control(self, action):
        try:
            self.render(call_timer(action, self.directory))
        except (ValueError, OSError) as error:
            messagebox.showerror('操作未完成', str(error), parent=self.root)

    def pause_resume(self):
        self.control('resume' if self.state == 'paused' else 'pause')

    def render(self, status):
        self.state = status.get('state', 'idle')
        self.active = self.state in ('focus', 'rest', 'paused')
        ended = self.state in ('ended', 'error')
        self.status_text.set({'focus': '学习中', 'rest': '短暂休息', 'paused': '已暂停',
                              'ended': '这次学习结束了', 'error': '计时器遇到问题'}.get(self.state, '准备好了，就开始。'))
        if not self.active:
            self.report_path = status.get('report_path') if ended else None
            for widget in (self.pause_button, self.defer_button, self.stop_button):
                widget.pack_forget()
            self.start_button.pack(side='left')
            if self.report_path:
                self.report_button.pack(anchor='w', pady=(12, 0))
            else:
                self.report_button.pack_forget()
            self.notice.set((status.get('error') or '可以起身走动、伸展或喝水。时间轴按需查看，复盘直接在 Agent 对话中进行。')
                            if ended else '只想复盘？直接在 Agent 中使用 $focus-session 即可。')
            for child in self.settings.winfo_children():
                if isinstance(child, (ttk.Entry, ttk.Checkbutton)):
                    child.state(['!disabled'])
            self.update_titles()
            if not sys.platform.startswith('win'):
                self.record_check.state(['disabled'])
        else:
            self.report_path = None
            self.report_button.pack_forget()
            self.start_button.pack_forget()
            for widget in (self.pause_button, self.defer_button, self.stop_button):
                widget.pack(side='left', padx=(0, 8))
            for child in self.settings.winfo_children():
                if isinstance(child, (ttk.Entry, ttk.Checkbutton)):
                    child.state(['disabled'])
            self.pause_button.configure(text='继续' if self.state == 'paused' else '暂停')
            self.defer_button.configure(text='跳过这次休息' if self.state == 'rest' else '稍后提醒')
            self.defer_button.state(['disabled'] if self.state == 'paused' else ['!disabled'])
            message = '可以最小化窗口。需要时，轻提示会响起。'
            if self.state == 'rest':
                message = '可以闭眼放松或把视线移开屏幕，听到恢复提示再继续；也可以跳过。'
            elif self.state == 'paused':
                message = (status.get('pause_reason') or '已暂停') + '。准备好后手动继续。'
            if status.get('recording_enabled'):
                message += ' 本次应用记录已开启。'
            self.notice.set(status.get('audio_warning') or message)

    def poll(self):
        try:
            current = call_timer('status', self.directory)
            # Discover externally started sessions, without reopening old reports.
            if self.active or current.get('state') in ('focus', 'rest', 'paused'):
                self.render(current)
        except (ValueError, OSError) as error:
            self.notice.set(str(error))
        self.after_id = self.root.after(1000, self.poll)

    def open_report(self):
        if self.report_path:
            webbrowser.open(Path(self.report_path).as_uri())

    def close(self):
        try:
            current = call_timer('status', self.directory)
            if current.get('state') in ('focus', 'rest', 'paused'):
                status = call_timer('stop', self.directory)
                self.report_path = status.get('report_path')
        except (ValueError, OSError) as error:
            messagebox.showerror('未能结束后台计时', str(error), parent=self.root)
            return
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.root.destroy()


def run_gui(directory=None):
    root = tk.Tk()
    FocusWindow(root, directory)
    root.mainloop()
