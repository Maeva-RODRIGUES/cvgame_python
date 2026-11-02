import subprocess
import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

BASE_DIR = Path(__file__).resolve().parent


class ReloadHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.start_process()

    def start_process(self):
        if self.process:
            self.process.kill()
        print("🚀 (Re)lancement de main.py")
        # CREATE_NEW_PROCESS_GROUP n'existe que sous Windows : ailleurs, aucune option
        flags = subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
        self.process = subprocess.Popen(
            [sys.executable, str(BASE_DIR / "main.py")], creationflags=flags
        )

    def on_modified(self, event):
        if event.src_path.endswith(".py") and not event.src_path.endswith("auto_reload.py"):
            print(f"🔁 Modification détectée dans {event.src_path}, rechargement...")
            self.start_process()


if __name__ == "__main__":
    path = str(BASE_DIR)
    event_handler = ReloadHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()
    print("👀 Surveillance en cours... (Ctrl+C pour arrêter)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Arrêt de la surveillance")
        observer.stop()
    observer.join()
