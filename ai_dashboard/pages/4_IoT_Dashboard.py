import streamlit as st
import requests
import time
import plotly.graph_objs as go
from ai_dashboard.config import IOT_SERVICE_URL

st.set_page_config(page_title="IoT Dashboard", layout="wide")

# -----------------------------------------
# Title
# -----------------------------------------
st.title("🚴 IoT Smart Gym – Live Equipment Dashboard")
st.write("Real-time sensor streaming from AI-powered gym equipment.")

# -----------------------------------------
# Sidebar: Machine + Controls
# -----------------------------------------
st.sidebar.header("⚙️ IoT Controls")

machine = st.sidebar.selectbox(
    "Choose Equipment",
    ["Treadmill", "Cycling", "Rowing", "Elliptical", "Dumbbells"]
)

duration = st.sidebar.slider("Streaming Duration (seconds)", 10, 120, 60)

# Initialize session state
if "stream_active" not in st.session_state:
    st.session_state.stream_active = False
if "stream_end_time" not in st.session_state:
    st.session_state.stream_end_time = 0
if "data" not in st.session_state:
    st.session_state.data = {"hr": [], "speed": [], "cal": [], "time": []}

# START STREAMING BUTTON
if st.sidebar.button("▶️ Start Streaming"):
    mach = machine.lower()
    requests.get(f"{IOT_SERVICE_URL}/iot/set-machine/{mach}")
    requests.get(f"{IOT_SERVICE_URL}/iot/stream/start/{mach}?duration={duration}")

    st.session_state.stream_active = True
    st.session_state.stream_end_time = time.time() + duration
    st.session_state.data = {"hr": [], "speed": [], "cal": [], "time": []}
    st.sidebar.success(f"Streaming started for {machine}!")

# STOP STREAMING BUTTON
if st.sidebar.button("⛔ Stop Streaming"):
    requests.get(f"{IOT_SERVICE_URL}/iot/stream/stop")
    st.session_state.stream_active = False
    st.sidebar.warning("Stream stopped manually.")

# -----------------------------------------
# Placeholders
# -----------------------------------------
status_box = st.empty()
timer_box = st.empty()
feedback_box = st.empty()

col1, col2 = st.columns(2)
chart_hr = col1.empty()
chart_cal = col2.empty()


# -----------------------------------------
# Helper functions
# -----------------------------------------
def fetch_status():
    try:
        r = requests.get(f"{IOT_SERVICE_URL}/iot/status", timeout=3)
        return r.json()
    except:
        return None


def plot_line(y, title, ylabel):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=y, mode="lines+markers"))
    fig.update_layout(
        title=title,
        xaxis_title="Time (s)",
        yaxis_title=ylabel,
        template="plotly_dark",
        height=300,
    )
    return fig


# -----------------------------------------
# STREAM LOOP
# -----------------------------------------
if st.session_state.stream_active:

    while time.time() < st.session_state.stream_end_time:

        time_left = int(st.session_state.stream_end_time - time.time())
        timer_box.markdown(
            f"""
            <h3>⏳ Time Left: <b>{time_left}s</b></h3>
            """,
            unsafe_allow_html=True
        )

        status = fetch_status()
        if not status:
            status_box.error("❌ Lost connection to IoT backend")
            break

        # update history
        t = status["session_elapsed"]
        st.session_state.data["time"].append(t)
        st.session_state.data["hr"].append(status["heart_rate"])
        st.session_state.data["speed"].append(status["speed"])
        st.session_state.data["cal"].append(status["total_calories"])

        # main status area
        status_box.markdown(f"""
        ### 📟 Live Status – {machine}
        - ❤️ **Heart Rate:** {status['heart_rate']} bpm  
        - 🏃 **Speed:** {status['speed']}  
        - 🔥 **Calories:** {round(status['total_calories'], 2)}  
        - 💪 **Reps:** {status['reps']}  
        - 😮‍💨 **Fatigue:** {status['fatigue']}  
        """)

        # AI FEEDBACK (single box)
        feedback_box.markdown(
            f"""
            <div style="
                background-color:#222; 
                padding:15px; 
                border-radius:10px;
                border:1px solid #444;
                font-size:18px;">
                <b>🧠 AI Feedback:</b><br>
                {status.get("ai_feedback", "Idle")}
            </div>
            """,
            unsafe_allow_html=True
        )

        # charts
        chart_hr.plotly_chart(
            plot_line(st.session_state.data["hr"], "Heart Rate", "BPM"),
            use_container_width=True
        )

        chart_cal.plotly_chart(
            plot_line(st.session_state.data["cal"], "Calories Burned", "kcal"),
            use_container_width=True
        )

        time.sleep(1)

    st.session_state.stream_active = False
    st.success("✅ Streaming session completed!")

else:
    st.info("Use the **sidebar** to start real-time streaming.")
