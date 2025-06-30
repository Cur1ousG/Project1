import streamlit as st
import time
import os
import pandas as pd
from datetime import datetime
from src.log_parser import summarize_log
from src.utils import ensure_directory

LOG_FILE = "logs/app.log"
TRENDS_FILE = "data/trends.csv"

ensure_directory("data")

st.set_page_config(page_title="📊 Log Monitor Dashboard", layout="wide")

def read_recent_lines(filepath, limit=100):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return lines[-limit:]
    except FileNotFoundError:
        return ["Log file not found."]

def update_trends_file(summary):
    today = datetime.now().strftime("%Y-%m-%d")
    new_row = {
        "date": today,
        "errors": len(summary['errors']),
        "warnings": len(summary['warnings']),
        "logins": len(summary['login_attempts'])
    }

    try:
        if os.path.exists(TRENDS_FILE):
            df = pd.read_csv(TRENDS_FILE)
            if today not in df['date'].values:
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        else:
            df = pd.DataFrame([new_row])
        df.to_csv(TRENDS_FILE, index=False)
    except Exception as e:
        print(f"⚠️ Could not update trends file: {e}")

def launch_dashboard():
    st.title("📊 Real-Time Log Dashboard")

    placeholder_summary = st.empty()
    placeholder_logs = st.empty()
    placeholder_chart = st.empty()

    while True:
        summary = summarize_log(LOG_FILE)
        update_trends_file(summary)

        with placeholder_summary.container():
            st.subheader("🔎 Summary")
            st.metric(label="Errors", value=len(summary['errors']))
            st.metric(label="Warnings", value=len(summary['warnings']))
            st.metric(label="Login Attempts", value=len(summary['login_attempts']))

        with placeholder_logs.container():
            st.subheader("📝 Recent Log Entries")
            st.code("\n".join(read_recent_lines(LOG_FILE)), language="text")

        with placeholder_chart.container():
            st.subheader("📈 Trends Over Time")
            if os.path.exists(TRENDS_FILE) and os.path.getsize(TRENDS_FILE) > 0:
                try:
                    df = pd.read_csv(TRENDS_FILE)
                    if not df.empty and all(col in df.columns for col in ["date", "errors", "warnings", "logins"]):
                        df["date"] = pd.to_datetime(df["date"])
                        df = df.sort_values("date")
                        st.line_chart(df.set_index("date"))
                    else:
                        st.warning("Trends file is empty or has invalid format.")
                except pd.errors.EmptyDataError:
                    st.warning("Trends file is empty. No data to display yet.")
                except Exception as e:
                    st.error(f"Error reading trend data: {e}")
            else:
                st.info("Trend data will appear after the first daily report is generated.")

        time.sleep(5)  # Refresh every 5 seconds