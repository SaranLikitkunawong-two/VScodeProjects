import yt_dlp
import tkinter as tk
from tkinter import filedialog


def download_mp3(url: str, output_folder: str):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
        "noplaylist": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def pick_folder() -> str:
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    folder = filedialog.askdirectory(title="Choose where to save the MP3")
    root.destroy()
    return folder


def main():
    url = input("Paste YouTube URL: ").strip()
    if not url:
        print("No URL provided. Exiting.")
        return

    folder = pick_folder()
    if not folder:
        print("No folder selected. Exiting.")
        return

    print(f"\nSaving to: {folder}\n")
    download_mp3(url, folder)
    print("\nDone!")


if __name__ == "__main__":
    main()
