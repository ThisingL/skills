# 提示音

保留原项目提示音素材，整场开始和结束使用同一段较长的提示音：

| 场景 | 原素材 | Windows 播放副本 |
| --- | --- | --- |
| 整场开始 | `long_rest_start.mp3` | `long_rest_start.wav` |
| 暂停后继续 | `short_rest_end.mp3` | `short_rest_end.wav` |
| 进入短休息 | `short_rest_start.mp3` | `short_rest_start.wav` |
| 短休息结束、跳过当前休息 | `short_rest_end.mp3` | `short_rest_end.wav` |
| 手动结束学习、达到整场时限 | `long_rest_start.mp3` | `long_rest_start.wav` |

所有文件位于 `assets/audio`。三个 MP3 与旧 Mac 版使用的 `short_rest_start.aiff` 均按原字节保留。三个 WAV 是原 MP3 的 16-bit PCM 解码副本，保持源文件采样率、声道和内容，不做音量归一化、剪辑或音色替换；AIFF 保留备查，Windows 不使用它。

Windows 通过标准库 [winsound 的异步文件播放](https://docs.python.org/3/library/winsound.html) 播放 WAV，不启动外部播放器。静音完全跳过播放；暂停中断当前声音；结束控制请求先返回、报告先保存，再让结束音播放完成。缺少文件或播放失败时报告错误，不自动换成另一种提示音。

分发时保留整个 `assets/audio`，使用者无需 FFmpeg。仅维护者需要从原 MP3 重新生成副本时，可执行 `ffmpeg -i <原文件.mp3> -map 0:a:0 -c:a pcm_s16le <同名.wav>`；不要增加调音、裁剪或变速参数。
