import os
import json
import fnmatch
from typing import List, Dict, Union
from collections import defaultdict

class FilePatternCrawler:
    def __init__(self, root_dir: str, patterns: List[str] = None,
                 update_every: int = 1000, save_path: str = "crawler_progress.json",
                 case_sensitive: bool = True, verbose: bool = True):
        self.root_dir = root_dir
        self.patterns = patterns or []
        self.update_every = update_every
        self.save_path = save_path
        self.case_sensitive = case_sensitive
        self.verbose = verbose

        self.matching_files = defaultdict(list)
        self.matching_dirs = defaultdict(list)
        self.processed_files = 0
        self.processed_dirs = 0

    def set_patterns(self, patterns: List[str]):
        self.patterns = patterns

    def load_previous_progress(self):
        if os.path.exists(self.save_path):
            with open(self.save_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.matching_files = defaultdict(list, data.get("files", {}))
                self.matching_dirs = defaultdict(list, data.get("folders", {}))
            if self.verbose:
                print(f"Loaded progress from '{self.save_path}'")

    def crawl(self):
        if not self.patterns:
            raise ValueError("No patterns set.")

        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            self.processed_dirs += 1
            self._process_path(dirpath, is_dir=True)

            for fname in filenames:
                self.processed_files += 1
                full_path = os.path.join(dirpath, fname)
                self._process_path(full_path, is_dir=False)

                if self.processed_files % self.update_every == 0:
                    self._save_progress()

        self._save_progress()
        if self.verbose:
            print("Crawl complete. Final save done.")

    def _process_path(self, path: str, is_dir: bool):
        try:
            name = os.path.basename(path)
            name = name if self.case_sensitive else name.lower()
            for pattern in self.patterns:
                pattern_check = pattern if self.case_sensitive else pattern.lower()
                match_fn = fnmatch.fnmatchcase if self.case_sensitive else fnmatch.fnmatch
                if match_fn(name, pattern_check):
                    target = self.matching_dirs if is_dir else self.matching_files
                    if path not in target[pattern]:
                        target[pattern].append(path)
        except Exception as e:
            if self.verbose:
                print(f"[{'Dir' if is_dir else 'File'} Error] {path}: {e}")

    def _save_progress(self):
        try:
            with open(self.save_path, "w", encoding="utf-8") as f:
                json.dump({
                    "files": self.matching_files,
                    "folders": self.matching_dirs
                }, f, indent=2)
            if self.verbose:
                print(f"Saved: {self.processed_files} files, {self.processed_dirs} folders")
        except Exception as e:
            if self.verbose:
                print(f"[Save Error] {self.save_path}: {e}")

    def get_summary_table(self) -> List[Dict[str, Union[str, str]]]:
        result = []
        for pattern, paths in self.matching_files.items():
            result.extend({"pattern": pattern, "type": "file", "path": p} for p in paths)
        for pattern, paths in self.matching_dirs.items():
            result.extend({"pattern": pattern, "type": "folder", "path": p} for p in paths)
        return result

    def to_dataframe(self):
        try:
            import pandas as pd
            return pd.DataFrame(self.get_summary_table())
        except ImportError:
            raise ImportError("Pandas is not installed. Use `pip install pandas`.")
