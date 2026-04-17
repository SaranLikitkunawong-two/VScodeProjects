import os
import yt_dlp
from pathlib import Path

MP3_QUALITIES = ["128", "192", "320"]
MP4_QUALITIES = ["720p", "1080p", "Best"]


def _mp4_format_string(quality: str) -> str:
    if quality == "720p":
        return "bestvideo[height<=720]+bestaudio/best[height<=720]"
    elif quality == "1080p":
        return "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
    else:
        return "bestvideo+bestaudio/best"


def download(url: str, fmt: str, quality: str, output_folder: str,
             on_progress=None, on_complete=None):
    """
    Download a YouTube video as MP3 or MP4.

    url:           YouTube URL
    fmt:           "mp3" or "mp4"
    quality:       "128" / "192" / "320" for mp3
                   "720p" / "1080p" / "Best" for mp4
    output_folder: destination directory path
    on_progress:   optional callback(d) — called repeatedly during download
    on_complete:   optional callback(filepath) — called once with the final file path
    """
    hooks = [on_progress] if on_progress else []
    outtmpl = str(Path(output_folder) / "%(title)s.%(ext)s")

    # Capture the final file path after post-processing (e.g. after FFmpeg converts
    # the audio to mp3, or merges video+audio into mp4). postprocessor_hooks fire
    # after each post-processor step with the updated info_dict.
    captured_path: list[str] = []

    def _postprocessor_hook(d: dict):
        if d["status"] == "finished":
            info = d.get("info_dict", {})
            path = info.get("filepath") or info.get("filename")
            if path and os.path.isfile(path):
                captured_path.append(path)

    if fmt == "mp3":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": outtmpl,
            "noplaylist": True,
            "progress_hooks": hooks,
            "postprocessor_hooks": [_postprocessor_hook],
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": quality,
            }],
        }
    else:  # mp4
        ydl_opts = {
            "format": _mp4_format_string(quality),
            "outtmpl": outtmpl,
            "noplaylist": True,
            "progress_hooks": hooks,
            "postprocessor_hooks": [_postprocessor_hook],
            "merge_output_format": "mp4",
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    if on_complete:
        # Fall back to the folder itself if we couldn't capture the exact file path
        final = captured_path[-1] if captured_path else output_folder
        on_complete(final)
