# ai-services/chat-service/app/personality.py

import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSONALITY_FILE = os.path.join(BASE_DIR, "data", "personality.json")

# Default personality style
DEFAULT_PERSONALITY = "friendly"


def load_personality():
    if not os.path.exists(PERSONALITY_FILE):
        return DEFAULT_PERSONALITY
    try:
        with open(PERSONALITY_FILE, "r") as f:
            data = json.load(f)
            return data.get("style", DEFAULT_PERSONALITY)
    except:
        return DEFAULT_PERSONALITY


def save_personality(style):
    with open(PERSONALITY_FILE, "w") as f:
        json.dump({"style": style}, f, indent=2)


# -----------------------------
# Helpers
# -----------------------------
def get_personality():
    return load_personality()


def detect_personality_change(message: str):
    """
    Detects if user is requesting a personality shift.
    """
    msg = message.lower()

    if "be friendly" in msg or "be nice" in msg:
        save_personality("friendly")
        return "friendly"
    if "be strict" in msg or "hardcore" in msg or "push me" in msg:
        save_personality("hardcore")
        return "hardcore"
    if "be calm" in msg or "relaxing" in msg:
        save_personality("calm")
        return "calm"
    if "be funny" in msg or "joke" in msg or "entertain" in msg:
        save_personality("funny")
        return "funny"

    return None


# -----------------------------
# Apply personality
# -----------------------------
def apply_personality(reply: str, style: str):
    """
    Applies personality tone ONLY ONCE.
    Avoids repeated prefixes like:
    - "I'm here with you"
    - duplicate emojis
    """

    signatures = {
        "friendly": "😊",
        "hardcore": "🔥",
        "calm": "🧘",
        "funny": "😄"
    }

    emoji = signatures.get(style, "😊")

    # If reply already starts with personality emoji → skip
    if reply.strip().startswith(tuple(signatures.values())):
        return reply

    # Apply personality once at the beginning
    return f"{emoji} {reply}"
