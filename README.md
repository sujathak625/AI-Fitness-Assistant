# 🏋️ AI Gym & Fitness Assistant

A complete **microservices-based fitness platform** featuring AI pose detection, diet planning, IoT integration, habit tracking, and a unified Streamlit dashboard.

This project follows a **Microservices Architecture** with multiple **FastAPI** backend services connected to a central **Streamlit** UI.

---

## 📋 Table of Contents

- Project Overview  
- Prerequisites  
- Installation  
- Project Structure  
- How to Run  
- Features & Testing  
- Configuration  
- **Mandatory Python Packages** ← *NEW*  

---

## 🌟 Project Overview

The platform includes the following components:

| Module | Description |
|--------|-------------|
| 🏋️ AI Workout Pose Detector | Real-time AI-based pose detection |
| 🥗 AI Diet Planner | Personalized meal plans using LLMs |
| 💬 AI Chat Assistant | Fitness + general chat assistant |
| 📊 Habit Tracker | Track and view daily habits |
| 🚴 IoT Smart Gym Dashboard | Live gym equipment telemetry via MQTT |
| 🏢 Gym Recommendation Service | Find gyms based on location + budget |
| 🎛️ Streamlit Dashboard | Unified UI |

---

## ⚙️ Prerequisites

- Python **3.10+**  
- macOS / Linux / Windows  
- Mosquitto MQTT Broker  

---

## 📦 Installation

### 1. Clone the Repo
```bash
git clone <your-repo-url>
cd ai-gym-and-fitness-assistant
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 📂 Project Structure

```
ai-gym-and-fitness-assistant/
│
├── start-services.sh
│
├── ai_dashboard/
│   ├── app.py
│   ├── config.py
│   └── pages/
│
└── ai-services/
    ├── pose-service/
    ├── diet-service/
    ├── habit-service/
    ├── chat-service/
    ├── iot-service/
    └── gym-service/
```

---

## 🚀 How to Run (Step-by-Step)

### Terminal 1 — MQTT Broker
```bash
mosquitto
```

### Terminal 2 — Backend Services
```bash
chmod +x start-services.sh
./start-services.sh
```

### Terminal 3 — Streamlit UI
```bash
cd ai_dashboard
streamlit run app.py
```

Open: http://localhost:8501

---

## 🧪 Features & Testing

| Feature | How to Test |
|---------|-------------|
| 🥗 Diet Planner | Ask: “I need a diet plan” in Chat Assistant |
| 🚴 IoT Streaming | Select machine → Start Streaming |
| 🏢 Gym Finder | Ask: “Gyms under 2000 in Bangalore” |
| 📊 Habit Tracker | Add → View summary |
| 🏋️ Pose Detector | Allow camera → Perform exercise |

---

## 🔧 Configuration

Edit:

`ai_dashboard/config.py`
```python
POSE_SERVICE_URL = "http://127.0.0.1:8000"
DIET_SERVICE_URL = "http://127.0.0.1:8100"
HABIT_SERVICE_URL = "http://127.0.0.1:8200"
CHAT_SERVICE_URL = "http://127.0.0.1:8300"
IOT_SERVICE_URL = "http://127.0.0.1:8500"
GYM_SERVICE_URL = "http://127.0.0.1:8600"
```

---

# 📦 Mandatory Python Packages  
*(Auto-generated from your local `pip list` — required for the project to run)*

```
absl-py 2.3.1
accelerate 1.11.0
altair 5.5.0
anyio 4.11.0
attrs 25.4.0
backports.asyncio.runner 1.2.0
blinker 1.9.0
cachetools 5.5.2
certifi 2025.11.12
cffi 2.0.0
charset-normalizer 3.4.4
click 8.3.1
contourpy 1.3.2
cycler 0.12.1
exceptiongroup 1.3.0
fastapi 0.110.0
filelock 3.20.0
flatbuffers 25.9.23
fonttools 4.60.1
fsspec 2025.10.0
gitdb 4.0.12
GitPython 3.1.45
h11 0.16.0
hf-xet 1.2.0
httpcore 1.0.9
httpx 0.28.1
huggingface-hub 0.36.0
idna 3.11
iniconfig 2.3.0
Jinja2 3.1.6
joblib 1.5.2
jsonschema 4.25.1
jsonschema-specifications 2025.9.1
kiwisolver 1.4.9
markdown-it-py 4.0.0
MarkupSafe 3.0.3
matplotlib 3.10.7
mdurl 0.1.2
mediapipe 0.10.8
mpmath 1.3.0
narwhals 2.12.0
networkx 3.3
nltk 3.9.1
numpy 1.26.4
opencv-contrib-python 4.8.1.78
opencv-python-headless 4.8.1.78
packaging 23.2
paho-mqtt 2.1.0
pandas 2.2.2
pillow 10.4.0
pip 25.3
plotly 5.19.0
pluggy 1.6.0
pose_service 0.1.0 (/Users/ksujatha/Projects/ai-gym-and-fitness-asistant/ai-services/pose-service)
protobuf 3.20.3
psutil 7.1.3
pyarrow 22.0.0
pycparser 2.23
pydantic 1.10.13
pydeck 0.9.1
Pygments 2.19.2
pyparsing 3.2.5
pytest 9.0.1
pytest-asyncio 1.3.0
python-dateutil 2.9.0.post0
python-multipart 0.0.9
pytz 2025.2
PyYAML 6.0.3
referencing 0.37.0
regex 2025.11.3
requests 2.31.0
rich 13.9.4
rpds-py 0.29.0
safetensors 0.7.0
sentencepiece 0.2.1
setuptools 80.9.0
six 1.17.0
smmap 5.0.2
sniffio 1.3.1
sounddevice 0.5.3
starlette 0.36.3
streamlit 1.32.0
sympy 1.14.0
tenacity 8.5.0
textblob 0.17.1
tokenizers 0.22.1
toml 0.10.2
tomli 2.3.0
torch 2.9.1
torchaudio 2.9.1
torchvision 0.24.1
tornado 6.5.2
tqdm 4.67.1
transformers 4.57.1
typing_extensions 4.15.0
tzdata 2025.2
urllib3 2.5.0
uvicorn 0.29.0
```

---
