import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time

class ReloadHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.start_process()

    def start_process(self):
        if self.process:
            self.process.kill()
        print("🚀 (Re)lancement de main.py")
        self.process = subprocess.Popen([sys.executable, "main.py"], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

    def on_modified(self, event):
        if event.src_path.endswith(".py") and not event.src_path.endswith("auto_reload.py"):
            print(f"🔁 Modification détectée dans {event.src_path}, rechargement...")
            self.start_process()

if __name__ == "__main__":
    path = "."
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
