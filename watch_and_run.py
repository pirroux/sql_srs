#!/usr/bin/env python3
"""
Simple file watcher that restarts Streamlit when Python files change.
Run this script instead of running streamlit directly.
"""

import subprocess
import time
import os
import signal
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class StreamlitHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.start_streamlit()
    
    def start_streamlit(self):
        if self.process:
            print("🔄 Restarting Streamlit...")
            self.process.terminate()
            self.process.wait()
        
        print("🚀 Starting Streamlit...")
        self.process = subprocess.Popen(
            ["streamlit", "run", "app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        # Start a thread to read output
        import threading
        def read_output():
            for line in iter(self.process.stdout.readline, ''):
                if line:
                    print(line.rstrip())
        
        thread = threading.Thread(target=read_output, daemon=True)
        thread.start()
    
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.py'):
            print(f"📝 File changed: {event.src_path}")
            self.start_streamlit()

def main():
    print("👀 Watching for changes in Python files...")
    print("Press Ctrl+C to stop")
    
    handler = StreamlitHandler()
    observer = Observer()
    observer.schedule(handler, path='.', recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping...")
        if handler.process:
            handler.process.terminate()
        observer.stop()
        observer.join()
        sys.exit(0)

if __name__ == "__main__":
    main()
