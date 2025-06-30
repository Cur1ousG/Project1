from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import re
import os

class LogEventHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        self.file_path = file_path
        self._last_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0

    def on_modified(self, event):
        if event.src_path == self.file_path:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                f.seek(self._last_size)
                new_lines = f.readlines()
                self._last_size = f.tell()

                for line in new_lines:
                    self.handle_log_line(line.strip())

    def handle_log_line(self, line):
        if re.search(r'\bERROR\b', line, re.IGNORECASE):
            print(f"[🔴 ERROR] {line}")
        elif re.search(r'\bWARNING\b', line, re.IGNORECASE):
            print(f"[🟠 WARNING] {line}")
        elif re.search(r'login|auth|signin|failed password', line, re.IGNORECASE):
            print(f"[🔐 LOGIN] {line}")

def start_monitoring(file_path):
    print(f"👀 Starting real-time monitoring: {file_path}")
    event_handler = LogEventHandler(file_path)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(file_path) or '.', recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()