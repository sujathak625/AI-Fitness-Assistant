def detect_emotion(text):
    t = text.lower()

    rules = {
        "excitement": ["great", "excited", "awesome", "motivated"],
        "sadness": ["sad", "upset", "unhappy"],
        "anxiety": ["worried", "nervous", "stressed"],
        "anger": ["angry", "mad", "frustrated"],
        "tired": ["tired", "exhausted", "sleepy"]
    }

    for emotion, words in rules.items():
        if any(w in t for w in words):
            return {"emotion": emotion, "score": 0.8}

    return {"emotion": "neutral", "score": 0.3}
