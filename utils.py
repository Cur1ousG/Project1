import os
from datetime import datetime
import csv

def get_timestamp():
    """Return current timestamp as formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_log_entry(log_line):
    """Clean and truncate log lines for display or storage."""
    return log_line.strip()[:200]

def ensure_directory(path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)

def sanitize_for_email(text):
    """Escape HTML characters to safely embed text in emails."""
    return text.replace("<", "&lt;").replace(">", "&gt;")

def append_to_csv(file_path, row_dict, headers):
    """
    Append a row dict to a CSV file, creating headers if needed.
    """
    file_exists = os.path.isfile(file_path)
    with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row_dict)