from pathlib import Path
import subprocess
import logging
import sys
import tkinter as tk
from tkinter import filedialog

VIDEO_EXTS = {".mp4", ".mov", ".mxf", ".mkv", ".avi"}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("proxy_creation.log", encoding="utf-8")
    ]
)

root = tk.Tk()
root.withdraw()

selected_folder = filedialog.askdirectory(title="Select source folder for proxy creation")

if not selected_folder:
    logging.info("No folder selected. Exiting.")
    raise SystemExit

SOURCE_DIR = Path(selected_folder)

videos = [p for p in SOURCE_DIR.rglob("*") if p.is_file() and p.suffix.lower() in VIDEO_EXTS and not p.stem.endswith("_proxy")]
total = len(videos)

proxy_dir = SOURCE_DIR / "proxies"
proxy_dir.mkdir(exist_ok=True)

logging.info("Selected source folder: %s", SOURCE_DIR)
logging.info("Proxy destination: %s", proxy_dir)
logging.info("Found %s video file(s)", total)

for index, video in enumerate(videos, start=1):
    stem = video.stem

    proxy_file = proxy_dir / f"{stem}_proxy.mov"

    if proxy_file.exists():
        logging.info("[%s/%s] Skipping existing proxy: %s", index, total, proxy_file)
        continue

    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(video),
        "-vf", "scale=1280:-2",
        "-c:v", "prores_ks",
        "-profile:v", "0",
        "-bits_per_mb", "8000", 
        "-pix_fmt", "yuv422p10le",
        "-c:a", "pcm_s16le",
        str(proxy_file)
    ]

    logging.info("[%s/%s] Creating proxy for: %s", index, total, video)

    try:
        subprocess.run(cmd, check=True)
        logging.info("[%s/%s] Finished: %s", index, total, proxy_file)
    except subprocess.CalledProcessError as e:
        logging.error("[%s/%s] FFmpeg failed for %s | return code: %s", index, total, video, e.returncode)
    except Exception as e:
        logging.exception("[%s/%s] Unexpected error for %s: %s", index, total, video, e)