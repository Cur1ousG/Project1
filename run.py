import subprocess
import threading
import time
import sys

def run_main():
    subprocess.run(["python", "src/main.py"])

def run_dashboard():
    subprocess.run([sys.executable, "-m", "streamlit", "run", "src/dashboard.py"])


threading.Thread(target=run_main, daemon=True).start()
time.sleep(3)

run_dashboard()