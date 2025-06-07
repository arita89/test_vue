import os
import re
import json
import fnmatch
import tkinter as tk
from tkinter import filedialog, ttk
from typing import List, Dict, Union
from collections import defaultdict

try:
    import pandas as pd
except ImportError:
    pd = None  # We check later before trying to export


class FilePatternCrawler:
    def __init__(self, root_dir: str, patterns: List[str] = None,
                 use_regex: bool = False, case_sensitive: bool = True,
                 update_every: int = 1000, save_path: str = "crawler_progress.json"):
        self.root_dir = root_dir
        self.patterns = patterns or []
        self.use_regex = use_regex
        self.case_sensitive = case_sensitive
        self.update_every = update_every
        self.save_path = save_path

        self.matching_files = defaultdict(list)
        self.matching_dirs = defaultdict(list)
        self.processed_files = 0
        self.processed_dirs = 0

    def crawl(self, on_progress=None):
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            self.processed_dirs += 1
            self._process_path(dirpath, is_dir=True)

            for fname in filenames:
                self.processed_files += 1
                full_path = os.path.join(dirpath, fname)
                self._process_path(full_path, is_dir=False)

                if self.processed_files % self.update_every == 0:
                    if on_progress:
                        on_progress(self.processed_files)
                    self._save_progress()

        self._save_progress()

    def _process_path(self, path: str, is_dir: bool):
        name = os.path.basename(path)
        if not self.case_sensitive:
            name = name.lower()

        for pattern in self.patterns:
            pattern_check = pattern if self.case_sensitive else pattern.lower()
            matched = False

            if self.use_regex:
                try:
                    if re.search(pattern_check, name):
                        matched = True
                except re.error:
                    continue
            else:
                match_fn = fnmatch.fnmatchcase if self.case_sensitive else fnmatch.fnmatch
                if match_fn(name, pattern_check):
                    matched = True

            if matched:
                target = self.matching_dirs if is_dir else self.matching_files
                if path not in target[pattern]:
                    target[pattern].append(path)

    def _save_progress(self):
        with open(self.save_path, "w", encoding="utf-8") as f:
            json.dump({
                "files": self.matching_files,
                "folders": self.matching_dirs
            }, f, indent=2)

    def to_dataframe(self):
        if not pd:
            raise ImportError("Pandas is not installed.")
        data = []
        for pattern, files in self.matching_files.items():
            for f in files:
                data.append({"pattern": pattern, "type": "file", "path": f})
        for pattern, dirs in self.matching_dirs.items():
            for d in dirs:
                data.append({"pattern": pattern, "type": "folder", "path": d})
        return pd.DataFrame(data)


class CrawlerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Pattern Crawler")
        self.root.geometry("600x400")
        self.folder_path = tk.StringVar()
        self.patterns = tk.StringVar()
        self.use_regex = tk.BooleanVar()
        self.case_sensitive = tk.BooleanVar(value=True)
        self.progress = tk.DoubleVar()
        self.results_df = None
        self._build_gui()
        self._enable_dark_mode()

    def _build_gui(self):
        tk.Label(self.root, text="Folder to search:").pack()
        folder_frame = tk.Frame(self.root)
        folder_frame.pack(fill="x")
        tk.Entry(folder_frame, textvariable=self.folder_path, width=50).pack(side="left", padx=5, pady=5)
        tk.Button(folder_frame, text="Browse", command=self.browse_folder).pack(side="right", padx=5)

        tk.Label(self.root, text="Patterns (comma-separated):").pack()
        tk.Entry(self.root, textvariable=self.patterns, width=50).pack(padx=5, pady=5)

        tk.Checkbutton(self.root, text="Use regex", variable=self.use_regex).pack()
        tk.Checkbutton(self.root, text="Case sensitive", variable=self.case_sensitive).pack()

        self.progressbar = ttk.Progressbar(self.root, orient="horizontal", mode="determinate", variable=self.progress)
        self.progressbar.pack(fill="x", padx=5, pady=10)

        self.status_label = tk.Label(self.root, text="Idle", anchor="w")
        self.status_label.pack(fill="x", padx=5)

        tk.Button(self.root, text="Start Crawling", command=self.run_crawler).pack(pady=5)
        self.export_btn = tk.Button(self.root, text="Export CSV", command=self.export_results, state="disabled")
        self.export_btn.pack(pady=5)

    def _enable_dark_mode(self):
        style = ttk.Style(self.root)
        try:
            style.theme_use('clam')
        except:
            pass
        bg = '#2e2e2e'
        fg = 'white'
        style.configure('.', background=bg, foreground=fg)
        style.configure('TEntry', fieldbackground='#444', foreground=fg)
        style.configure('TLabel', background=bg, foreground=fg)
        style.configure('TButton', background='#555', foreground=fg)
        self.root.configure(bg=bg)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def run_crawler(self):
        self.progress.set(0)
        self.status_label.config(text="Crawling...")
        self.export_btn.config(state="disabled")
        self.root.update()

        folder = self.folder_path.get()
        pattern_list = [p.strip() for p in self.patterns.get().split(",") if p.strip()]

        if not folder or not pattern_list:
            self.status_label.config(text="Please select a folder and enter patterns.")
            return

        crawler = FilePatternCrawler(
            root_dir=folder,
            patterns=pattern_list,
            use_regex=self.use_regex.get(),
            case_sensitive=self.case_sensitive.get(),
            update_every=500
        )

        total_estimate = sum(len(files) for _, _, files in os.walk(folder))

        def update_progress(count):
            percent = (count / total_estimate) * 100 if total_estimate else 0
            self.progress.set(min(percent, 100))
            self.root.update_idletasks()

        crawler.crawl(on_progress=update_progress)

        try:
            self.results_df = crawler.to_dataframe()
            self.status_label.config(text=f"Done. Found {len(self.results_df)} matches.")
            self.export_btn.config(state="normal")
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")

    def export_results(self):
        if self.results_df is not None and not self.results_df.empty:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv")
            if file_path:
                self.results_df.to_csv(file_path, index=False)
                self.status_label.config(text=f"Exported to {file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CrawlerGUI(root)
    root.mainloop()
