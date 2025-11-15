from fastapi import FastAPI
from pydantic import BaseModel
from .nlp import generate_ai_reply
from .emotions import detect_emotion

app = FastAPI(title="AI Chat Service")

class ChatRequest(BaseModel):
    msg: str

@app.get("/health")
def health():
    return {"status": "ok", "service": "chat-service"}

@app.post("/chat/respond")
def chat_reply(payload: ChatRequest):
    user_msg = payload.msg

    reply_data = generate_ai_reply(user_msg)

    # If simple string returned
    if isinstance(reply_data, str):
        reply_payload = {"reply": reply_data}
    else:
        reply_payload = reply_data

    # Emotion detection layer
    emo = detect_emotion(user_msg)
    reply_payload["emotion"] = emo.get("emotion", "neutral")
    reply_payload["score"] = emo.get("score", 0.0)

    return reply_payload
