import streamlit as st
import requests
import time
from ai_dashboard.config import CHAT_SERVICE_URL

# ---------- badges ----------
def emotion_badge(emotion):
    badges = {
        "sadness": "🔵 Sad",
        "anger": "🔴 Angry",
        "tired": "🟠 Tired",
        "excitement": "🟢 Excited",
        "neutral": "⚪ Neutral"
    }
    return badges.get(emotion, "⚪ Neutral")

def personality_badge(style):
    badges = {
        "friendly": "😊",
        "hardcore": "🔥",
        "calm": "🧘",
        "funny": "😄"
    }
    return badges.get(style, "😊")

def goal_badge(goal):
    badges = {
        "fat_loss": "🔥 Fat Loss",
        "muscle_gain": "💪 Muscle Gain",
        "maintenance": "⚖️ Maintenance",
        "endurance": "🏃 Endurance"
    }
    return badges.get(goal, "")

# ---------- typing animation ----------
def typewriter(text, delay=0.004):
    placeholder = st.empty()
    cur = ""
    for c in text:
        cur += c
        placeholder.markdown(cur)
        time.sleep(delay)
    return cur

# ---------- floating chat widget ----------
def chat_widget():

    # State: chat open?
    if "chat_open" not in st.session_state:
        st.session_state.chat_open = False

    # State: messages
    if "widget_messages" not in st.session_state:
        st.session_state.widget_messages = []

    # ---------- FLOATING BUTTON ----------
    st.markdown("""
        <style>
        .chat-btn {
            position: fixed;
            bottom: 25px;
            right: 25px;
            background-color: #4CAF50;
            color: white;
            font-size: 26px;
            border-radius: 50%;
            padding: 14px 18px;
            cursor: pointer;
            z-index: 9999;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        </style>
        <div class="chat-btn" onclick="window.parent.postMessage({type:'toggle_chat'}, '*')">
            💬
        </div>
    """, unsafe_allow_html=True)

    # JS → toggles chat window by updating session_state
    st.markdown("""
        <script>
        document.addEventListener("DOMContentLoaded", function() {
            window.addEventListener("message", (event) => {
                if (event.data.type === "toggle_chat") {
                    const streamlitEvent = new Event("streamlit_toggle_chat");
                    document.dispatchEvent(streamlitEvent);
                }
            });
        });
        </script>
    """, unsafe_allow_html=True)

    # Streamlit listener
    if "chat_listener_set" not in st.session_state:
        st.session_state.chat_listener_set = True

        # Use custom listener
        st.rerun()

    # Toggle via JS trigger (Streamlit can't detect JS directly)
    st.session_state.chat_open = True

    # ---------- CHAT BOX UI ----------
    if st.session_state.chat_open:

        st.markdown("""
            <div style="
                position: fixed;
                bottom: 90px;
                right: 25px;
                width: 330px;
                background: white;
                border-radius: 12px;
                padding: 15px;
                box-shadow: 0px 4px 15px rgba(0,0,0,0.25);
                z-index: 9998;
            ">
        """, unsafe_allow_html=True)

        st.write("### 💬 Gym Buddy Chat")

        # -----------------------------------------------
        # DISPLAY MESSAGE HISTORY
        # -----------------------------------------------
        for msg in st.session_state.widget_messages:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['text']}")
            else:
                st.markdown(msg["text"])

        # -----------------------------------------------
        # INPUT BOX
        # -----------------------------------------------
        user_input = st.text_input("Type here:", key="chat_input_widget")

        if user_input:
            st.session_state.widget_messages.append({"role": "user", "text": user_input})

            try:
                res = requests.post(
                    f"{CHAT_SERVICE_URL}/chat/respond",
                    json={"message": user_input},
                    timeout=8
                ).json()

                # Format response
                fmt = (
                    f"{emotion_badge(res['sentiment'])} "
                    f"{personality_badge(res['personality'])} "
                    f"{goal_badge(res['goal'])}<br><br>"
                    f"{res['reply']}"
                )

                if res.get("motivation"):
                    fmt += f"<br><br>💡 {res['motivation']}"

                typewriter(fmt)

                st.session_state.widget_messages.append({"role": "bot", "text": fmt})

                # Clear input
                st.session_state.chat_input_widget = ""
                st.rerun()

            except Exception as e:
                st.error(f"Chat error: {e}")

        st.markdown("</div>", unsafe_allow_html=True)
