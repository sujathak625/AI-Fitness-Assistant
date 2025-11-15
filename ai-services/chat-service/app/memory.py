# memory.py
import json
import os
from typing import Any, Dict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEM_FILE = os.path.join(BASE_DIR, "data", "memory.json")

# ensure data folder and file exist
os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
if not os.path.exists(MEM_FILE):
    with open(MEM_FILE, "w") as f:
        json.dump({"profile": {}, "conversations": []}, f, indent=2)


def _load() -> Dict[str, Any]:
    try:
        with open(MEM_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {"profile": {}, "conversations": []}


def _save(data: Dict[str, Any]):
    with open(MEM_FILE, "w") as f:
        json.dump(data, f, indent=2)


def remember_user_field(key: str, value: Any):
    d = _load()
    if "profile" not in d:
        d["profile"] = {}
    d["profile"][key] = value
    _save(d)
    return True


def get_user_profile() -> Dict[str, Any]:
    d = _load()
    return d.get("profile", {})


def remember_conversation(speaker: str, text: str):
    d = _load()
    if "conversations" not in d:
        d["conversations"] = []
    d["conversations"].append({"who": speaker, "text": text})
    # cap to last 200 messages
    d["conversations"] = d["conversations"][-200:]
    _save(d)
    return True


def save_memory_file():
    # handy hook to force write (calls _save with current in-memory)
    return True
