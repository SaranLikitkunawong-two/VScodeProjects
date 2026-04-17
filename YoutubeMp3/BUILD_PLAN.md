# YouTube Downloader App — Build Plan

## What are we building?

A **desktop GUI application** that lets you:
- Paste one or more YouTube URLs
- Choose MP3 or MP4
- Choose quality (audio bitrate for MP3, video resolution for MP4)
- Pick a save folder
- Watch downloads progress

Yes — the final deliverable is an **executable file** (`.exe` on Windows). You double-click it, the app opens, no Python installation needed. This is called **packaging** or **bundling** your app.

---

## Key Decisions You Need to Make

These are the architectural choices. Each has trade-offs. I'll explain each one so you understand *why* it matters, not just *what* to pick.

---

### Decision 1: GUI Framework

This is the biggest decision. The GUI framework is the library that draws the window, buttons, input fields, etc.

| Option | Look | Learning Curve | Notes |
|--------|------|----------------|-------|
| **tkinter** (you already use this) | Dated/plain | Low | Built into Python — no install needed. Works but ugly by default. |
| **CustomTkinter** | Modern, clean | Low | Drop-in upgrade from tkinter. Looks like a real modern app. Easiest path forward. |
| **PyQt6** | Professional, native-ish | Medium | Industry-standard. More powerful, more complex. |
| **Dear PyGui** | GPU-rendered, unique | Medium | Very fast, game-dev style, but unusual for desktop utilities. |

**Recommendation: CustomTkinter**

Why: You already know tkinter's mental model. CustomTkinter is literally `import customtkinter as ctk` instead of `import tkinter as tk`, and your widgets look modern with almost zero changes. For a learning project that you want to actually finish and use, this is the pragmatic choice.

If you later want to go deeper into GUI development, PyQt6 is worth learning — but it has a steeper ramp.

---

### Decision 2: App Architecture (Single File vs. Separated)

You can write everything in one Python file, or split it up.

**Option A — Single file (`app.py`)**
- All GUI code and download logic in one place
- Fine for small apps
- Gets messy as features grow

**Option B — Separated (recommended)**
```
YoutubeMp3/
├── app.py           # Entry point — just starts the window
├── ui/
│   └── main_window.py   # All the GUI layout and interaction
├── downloader.py    # All yt_dlp logic (no GUI code here)
└── BUILD_PLAN.md
```

**Why separation matters:** Your download logic (yt_dlp) has nothing to do with buttons and layouts. If you keep them separate, you can change the GUI without touching download logic, and vice versa. This is called **separation of concerns** — one of the most important concepts in software architecture.

---

### Decision 3: Threading (Critical — Don't Skip This)

Downloads take time. If you run a download directly in your GUI code, the entire window **freezes** until the download finishes. The user can't click anything, can't see progress, can't cancel.

The solution: run downloads on a **background thread**, keeping the UI responsive.

Python has two main tools for this:
- `threading.Thread` — simple, low-level, fine for this use case
- `asyncio` — more powerful but more complex, overkill here

**Recommendation: `threading.Thread`**

The pattern looks like:
```python
import threading

def start_download():
    thread = threading.Thread(target=run_download, daemon=True)
    thread.start()
```

`daemon=True` means the thread dies automatically when you close the app — without it, the app process can hang open invisibly after you close the window.

---

### Decision 4: Progress Reporting

yt_dlp can call a function you provide as it downloads, giving you percentage, speed, ETA, etc. This is called a **progress hook**.

You'll need to route that information from the background thread back to the UI. The pattern is a **thread-safe queue**:

```
Download thread → puts updates in Queue → UI thread reads Queue → updates progress bar
```

tkinter/CustomTkinter is not thread-safe — you cannot directly update a widget from a background thread or the app will crash or behave unpredictably. The queue pattern solves this cleanly.

---

### Decision 5: Multiple URLs

Do you want to download one URL at a time, or queue multiple?

- **Single URL**: Simpler. User pastes URL, downloads, done.
- **Queue (multi-URL)**: User pastes several URLs, app downloads them one by one (or in parallel). More useful but more complex to build.

**Recommendation: Start with single URL, design the code so it's easy to add queue later.**

The key is: don't hardcode assumptions that make queuing impossible. E.g., don't use global variables for "the current URL" — use a list even if it only ever has one item at first.

---

### Decision 6: Packaging Tool (How to make the .exe)

Once the app works, you need to bundle Python + your code + all dependencies into a single executable.

| Tool | Pros | Cons |
|------|------|------|
| **PyInstaller** | Most popular, well-documented, simple CLI | .exe can be large (50-150MB) |
| **cx_Freeze** | Similar to PyInstaller | Less documentation, more config |
| **Nuitka** | Compiles to actual native code, faster | Complex, longer build times |

**Recommendation: PyInstaller**

Command to build (once everything works):
```bash
pyinstaller --onefile --windowed app.py
```

- `--onefile` = bundle everything into a single `.exe`
- `--windowed` = don't show a terminal/console window behind your app

**Note:** yt_dlp requires **FFmpeg** to convert audio. FFmpeg is a separate binary. You'll need to either:
1. Tell users to install FFmpeg separately (less user-friendly), or
2. Bundle FFmpeg inside your `.exe` with PyInstaller (more work, but self-contained)

We'll handle this in the packaging step.

---

## Proposed Feature Set (MVP)

Start with this. Don't add more until this works:

- [ ] Window with a URL input field
- [ ] Format selector: MP3 / MP4
- [ ] Quality selector:
  - MP3: 128 kbps / 192 kbps / 320 kbps
  - MP4: 720p / 1080p / Best available
- [ ] Output folder picker (already have this)
- [ ] Download button
- [ ] Progress bar + status text
- [ ] Cancel button (stops the thread)

---

## Proposed File Structure

```
YoutubeMp3/
├── app.py                # Entry point
├── downloader.py         # yt_dlp wrapper (format, quality, progress hook)
├── ui/
│   └── main_window.py    # CustomTkinter window layout
├── requirements.txt      # yt-dlp, customtkinter
├── BUILD_PLAN.md         # This file
└── dist/                 # PyInstaller output (generated, not committed)
    └── YouTubeDownloader.exe
```

---

## Build Order (Step by Step)

### Step 1 — Install dependencies
```bash
pip install customtkinter yt-dlp
```

### Step 2 — Build `downloader.py`
Port your existing `download_mp3` function. Extend it to handle:
- Format (mp3 vs mp4)
- Quality selection
- Progress hook callback

### Step 3 — Build `ui/main_window.py`
Layout all the widgets. Wire up buttons to call functions (but don't put download logic here — call `downloader.py`).

### Step 4 — Add threading
Wrap the download call in a background thread. Use a `queue.Queue` to send progress updates back to the UI.

### Step 5 — Test it as a Python script
Run `python app.py` and verify everything works before packaging.

### Step 6 — Package with PyInstaller
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "YouTubeDownloader" app.py
```

The `.exe` will appear in the `dist/` folder.

---

## What You'll Learn

By the end of this project you will have hands-on experience with:

- **GUI programming** with tkinter/CustomTkinter
- **Separation of concerns** (UI vs. logic)
- **Threading** in Python
- **Thread-safe communication** with queues
- **Callbacks / hooks** (yt_dlp's progress hook is a great real-world example)
- **Packaging Python apps** into executables with PyInstaller

These are all transferable skills — they show up in virtually every Python desktop or automation project.

---

## Next Steps

When you're ready to start coding, say the word and we'll begin with Step 2 (`downloader.py`) since you already understand that piece best. We'll build bottom-up: logic first, UI second, packaging last.
