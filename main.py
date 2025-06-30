import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.log_parser import summarize_log
from src.email_report import send_html_email_with_pdf
from src.live_monitor import start_monitoring
from src.dashboard import launch_dashboard
from src.utils import ensure_directory
import schedule
import time
import threading
import os

LOG_FILE = "logs/app.log"

ensure_directory("logs")
ensure_directory("reports")
ensure_directory("data")

def daily_job():
    summary = summarize_log(LOG_FILE)
    send_html_email_with_pdf(summary)

schedule.every().day.at("08:00").do(daily_job)

threading.Thread(target=start_monitoring, args=(LOG_FILE,), daemon=True).start()

while True:
    schedule.run_pending()
    time.sleep(60)