import os
import queue
import subprocess
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox

import downloader


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("YouTube Downloader")
        self.geometry("680x600")
        self.resizable(True, True)
        self.minsize(520, 480)

        self._appearance = "dark"
        self._output_folder = ""
        self._items: list[dict] = []        # one entry per queued download, main-thread only
        self._progress_queue: queue.Queue = queue.Queue()   # worker → UI
        self._work_queue: queue.Queue = queue.Queue()       # UI → worker

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self._build_ui()
        self._launch_worker()   # persistent daemon thread, waits for work
        self._poll_progress()   # tkinter after()-loop, reads progress_queue

    # ------------------------------------------------------------------ #
    #  UI Construction                                                     #
    # ------------------------------------------------------------------ #

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)  # queue frame is the expanding row

        # --- Top bar ---
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.grid(row=0, column=0, padx=16, pady=(16, 0), sticky="ew")
        top.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(top, text="YouTube Downloader",
                     font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, sticky="w")
        self._theme_btn = ctk.CTkButton(top, text="Light Mode", width=110,
                                        command=self._toggle_theme)
        self._theme_btn.grid(row=0, column=1, sticky="e")

        # --- URL input ---
        ctk.CTkLabel(self, text="URLs  (one per line)",
                     font=ctk.CTkFont(size=13)).grid(row=1, column=0, padx=16, pady=(14, 4), sticky="w")
        self._url_box = ctk.CTkTextbox(self, height=90, font=ctk.CTkFont(size=12))
        self._url_box.grid(row=2, column=0, padx=16, sticky="ew")

        # --- Controls: format, quality, folder button ---
        ctrl = ctk.CTkFrame(self, fg_color="transparent")
        ctrl.grid(row=3, column=0, padx=16, pady=(10, 4), sticky="ew")

        ctk.CTkLabel(ctrl, text="Format").grid(row=0, column=0, padx=(0, 4), sticky="w")
        self._fmt_var = ctk.StringVar(value="mp3")
        ctk.CTkOptionMenu(ctrl, values=["mp3", "mp4"], variable=self._fmt_var,
                          width=80, command=self._on_format_change).grid(row=0, column=1, padx=(0, 20))

        ctk.CTkLabel(ctrl, text="Quality").grid(row=0, column=2, padx=(0, 4), sticky="w")
        self._quality_var = ctk.StringVar(value="192")
        self._quality_menu = ctk.CTkOptionMenu(ctrl, values=downloader.MP3_QUALITIES,
                                               variable=self._quality_var, width=90)
        self._quality_menu.grid(row=0, column=3, padx=(0, 20))

        ctk.CTkButton(ctrl, text="Browse Folder", width=110,
                      command=self._pick_folder).grid(row=0, column=4)

        # --- Folder path display ---
        self._folder_lbl = ctk.CTkLabel(self, text="No folder selected", anchor="w",
                                        font=ctk.CTkFont(size=11), text_color="gray60")
        self._folder_lbl.grid(row=4, column=0, padx=16, pady=(0, 4), sticky="ew")

        # --- Add to Queue button ---
        ctk.CTkButton(self, text="Add to Queue  →", height=34,
                      command=self._add_to_queue).grid(row=5, column=0, padx=16, pady=(4, 8), sticky="e")

        # --- Queue header ---
        q_header = ctk.CTkFrame(self, fg_color="transparent")
        q_header.grid(row=6, column=0, padx=16, pady=(0, 4), sticky="ew")
        q_header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(q_header, text="Queue",
                     font=ctk.CTkFont(size=13, weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(q_header, text="Clear Done", width=90, height=28,
                      command=self._clear_done).grid(row=0, column=1, sticky="e")

        # --- Queue list ---
        self._queue_frame = ctk.CTkScrollableFrame(self)
        self._queue_frame.grid(row=7, column=0, padx=16, pady=(0, 16), sticky="nsew")
        self._queue_frame.grid_columnconfigure(0, weight=1)

    # ------------------------------------------------------------------ #
    #  Event Handlers                                                      #
    # ------------------------------------------------------------------ #

    def _toggle_theme(self):
        self._appearance = "light" if self._appearance == "dark" else "dark"
        ctk.set_appearance_mode(self._appearance)
        self._theme_btn.configure(
            text="Dark Mode" if self._appearance == "light" else "Light Mode"
        )

    def _on_format_change(self, fmt: str):
        """Swap quality options when the user switches between mp3 and mp4."""
        values = downloader.MP3_QUALITIES if fmt == "mp3" else downloader.MP4_QUALITIES
        self._quality_menu.configure(values=values)
        self._quality_var.set(values[1])  # middle option as default

    def _pick_folder(self):
        folder = filedialog.askdirectory(title="Choose save folder")
        if folder:
            self._output_folder = folder
            display = folder if len(folder) < 60 else "…" + folder[-57:]
            self._folder_lbl.configure(text=display, text_color=("gray20", "gray80"))

    def _add_to_queue(self):
        urls = [u.strip() for u in self._url_box.get("1.0", "end").splitlines() if u.strip()]
        if not urls:
            messagebox.showwarning("No URLs", "Paste at least one URL first.")
            return
        if not self._output_folder:
            messagebox.showwarning("No Folder", "Choose a save folder first.")
            return

        fmt = self._fmt_var.get()
        quality = self._quality_var.get()

        for url in urls:
            idx = len(self._items)
            item = {
                "url": url, "fmt": fmt, "quality": quality,
                "folder": self._output_folder,
                "row_frame": None, "status_label": None,
            }
            self._items.append(item)
            self._add_queue_row(item, idx)
            self._work_queue.put((idx, item))  # hand off to worker

        self._url_box.delete("1.0", "end")

    def _add_queue_row(self, item: dict, idx: int):
        """Add a single row to the queue display and store widget refs in the item dict."""
        row = ctk.CTkFrame(self._queue_frame, corner_radius=6)
        row.grid(row=idx, column=0, padx=4, pady=3, sticky="ew")
        row.grid_columnconfigure(0, weight=1)

        url = item["url"]
        short_url = url if len(url) <= 60 else url[:57] + "..."
        url_lbl = ctk.CTkLabel(row, text=short_url, anchor="w", font=ctk.CTkFont(size=11))
        url_lbl.grid(row=0, column=0, padx=8, pady=6, sticky="ew")

        status_lbl = ctk.CTkLabel(row, text="Pending", width=150, anchor="e",
                                  font=ctk.CTkFont(size=11), text_color="gray60")
        status_lbl.grid(row=0, column=1, padx=(0, 8), pady=6)

        item["row_frame"] = row
        item["url_label"] = url_lbl
        item["status_label"] = status_lbl

    def _clear_done(self):
        """Hide completed and errored rows without removing them from self._items.
        Keeping items in the list preserves indices so in-progress updates stay correct."""
        for item in self._items:
            lbl = item.get("status_label")
            if lbl and lbl.cget("text") in ("Done ✓  📂", "Error"):
                item["row_frame"].grid_remove()

    def _make_row_clickable(self, idx: int, filepath: str):
        """Called once a download finishes. Wires up click → open in Explorer."""
        item = self._items[idx]
        item["filepath"] = filepath

        def open_in_explorer(event=None, p=filepath):
            if os.path.isfile(p):
                # /select highlights the specific file in the folder
                subprocess.Popen(["explorer", f"/select,{p}"])
            else:
                subprocess.Popen(["explorer", p])

        for widget in [item["row_frame"], item["url_label"], item["status_label"]]:
            widget.configure(cursor="hand2")
            widget.bind("<Button-1>", open_in_explorer)

    # ------------------------------------------------------------------ #
    #  Worker Thread                                                       #
    # ------------------------------------------------------------------ #

    def _launch_worker(self):
        """Start a single persistent daemon thread that processes the work queue."""
        threading.Thread(target=self._worker_loop, daemon=True).start()

    def _worker_loop(self):
        """Runs on the worker thread. Blocks on work_queue.get() between downloads."""
        while True:
            idx, item = self._work_queue.get()

            self._progress_queue.put({"index": idx, "text": "Starting...", "color": "#3B8ED0"})

            # i=idx captures the current value of idx in this iteration (loop closure fix)
            def on_progress(d, i=idx):
                self._progress_queue.put({"index": i, "data": d})

            def on_complete(path, i=idx):
                self._progress_queue.put({"index": i, "filepath": path})

            try:
                downloader.download(
                    url=item["url"],
                    fmt=item["fmt"],
                    quality=item["quality"],
                    output_folder=item["folder"],
                    on_progress=on_progress,
                    on_complete=on_complete,
                )
                self._progress_queue.put({"index": idx, "text": "Done ✓  📂", "color": "#2ECC71"})
            except Exception:
                self._progress_queue.put({"index": idx, "text": "Error", "color": "#E74C3C"})

            self._work_queue.task_done()

    # ------------------------------------------------------------------ #
    #  Progress Polling                                                    #
    # ------------------------------------------------------------------ #

    def _poll_progress(self):
        """Called every 100ms by tkinter's event loop. Drains progress_queue and updates labels.
        This is the only place we touch UI widgets from queued data — always on the main thread."""
        try:
            while True:
                msg = self._progress_queue.get_nowait()
                idx = msg["index"]
                if idx >= len(self._items):
                    continue
                lbl = self._items[idx]["status_label"]
                if lbl is None:
                    continue

                if "data" in msg:
                    # Raw yt_dlp progress dict
                    d = msg["data"]
                    if d.get("status") == "downloading":
                        pct = d.get("_percent_str", "").strip()
                        speed = d.get("_speed_str", "").strip()
                        lbl.configure(text=f"{pct}  {speed}", text_color="#3B8ED0")
                    elif d.get("status") == "finished":
                        lbl.configure(text="Processing...", text_color="orange")
                elif "filepath" in msg:
                    # Final file path captured — wire up click to open in Explorer
                    self._make_row_clickable(idx, msg["filepath"])
                else:
                    # Simple status message (Starting, Done, Error)
                    lbl.configure(text=msg["text"], text_color=msg["color"])

        except queue.Empty:
            pass

        self.after(100, self._poll_progress)
