import streamlit as st
import pandas as pd
import requests
from ai_dashboard.config import HABIT_SERVICE_URL

st.title("📊 Habit Tracker")
st.write("Track your daily fitness habits, logs, and progress.")

# ---------------------------------------
# Load logs from backend
# ---------------------------------------
def load_logs():
    try:
        res = requests.get(f"{HABIT_SERVICE_URL}/habits/logs")
        data = res.json()
        return data.get("logs", [])
    except Exception as e:
        st.error(f"Error loading logs: {e}")
        return []

# ---------------------------------------
# Save new log
# ---------------------------------------
def add_log(habit, status):
    try:
        res = requests.post(
            f"{HABIT_SERVICE_URL}/habits/log",
            json={"habit": habit, "status": status},
            timeout=5
        )
        return res.json()
    except Exception as e:
        st.error(f"Error saving log: {e}")
        return None

# ---------------------------------------
# UI: NEW LOG
# ---------------------------------------
st.subheader("📝 Add New Habit Log")

col1, col2 = st.columns(2)
with col1:
    habit = st.text_input("Habit (Example: Running, Yoga, Steps)")
with col2:
    status = st.selectbox("Status", ["Completed", "Skipped", "Partial"])

if st.button("Add Log"):
    if not habit:
        st.warning("Please enter a habit.")
    else:
        add_log(habit, status)
        st.success("Habit log added!")
        st.rerun()

# ---------------------------------------
# DISPLAY ALL LOGS
# ---------------------------------------
st.subheader("📅 Habit History")

logs = load_logs()

if not logs:
    st.info("No habit logs available.")
else:
    df = pd.DataFrame(logs)

    # -------------------------
    # FIX: Parse ISO timestamps correctly
    # -------------------------
    df["date"] = pd.to_datetime(df["date"], format="ISO8601")
    df["date"] = df["date"].dt.strftime("%Y-%m-%d %H:%M")

    st.dataframe(df, use_container_width=True)

# ---------------------------------------
# Summary Section
# ---------------------------------------
if logs:
    st.subheader("📈 Summary")

    completed = sum(1 for l in logs if l["status"] == "Completed")
    skipped = sum(1 for l in logs if l["status"] == "Skipped")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Completed", completed)
    with col2:
        st.metric("Skipped", skipped)
