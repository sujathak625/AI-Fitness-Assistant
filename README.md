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

- Python **3.10+**  (Do not run in latest python. Only Version 3.10 will be required as some of the libraries used will not work with latest version)
- macOS / Linux / Windows  
- Mosquitto MQTT Broker  

---

## 📦 Installation

### 1. Clone the Repo
```bash
git clone https://github.com/sujathak625/AI-Fitness-Assistant.git
cd AI-Fitness-Assistant
```

### 2. Create Virtual Environment

Due to librariy compatiblity, this project works with Python 3.10 only.

```bash
python3.10 -m venv .venv      

source .venv/bin/activate    # For Mac
```

### 3. Install Dependencies


# 📦 Mandatory Dependencies (Grouped)

Below are all required Python libraries for this project, grouped logically for clarity.

---

## 🔧 Install All Dependencies Before Running the Project

```bash
pip install -r requirements.txt
```

Make sure you run this **inside your virtual environment (`.venv`)**.

---

# 📚 Dependency Groups (Markdown Tables)

---

## 1️⃣ Core Backend Frameworks (API Layer)

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.110.0 | Main backend framework |
| uvicorn | 0.29.0 | ASGI server |
| starlette | 0.36.3 | FastAPI's core toolkit |
| anyio | 4.11.0 | Async event loop |
| h11 | 0.16.0 | HTTP/1.1 protocol |
| httpx | 0.28.1 | Async API client |
| httpcore | 1.0.9 | HTTP transport layer |

---

## 2️⃣ Frontend & Visualization (Streamlit UI)

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.32.0 | Main dashboard UI |
| altair | 5.5.0 | Visualizations & charts |
| plotly | 5.19.0 | Interactive graphs |
| pydeck | 0.9.1 | 3D & geographical maps |
| blinker | 1.9.0 | Event handling (Streamlit) |
| tornado | 6.5.2 | Websocket backend |
| rich | 13.9.4 | Modern console printing |

---

## 3️⃣ AI / Machine Learning / NLP / Transformers

| Package | Version | Purpose |
|---------|---------|---------|
| torch | 2.9.1 | Deep learning |
| torchvision | 0.24.1 | Vision utilities |
| torchaudio | 2.9.1 | Audio processing |
| transformers | 4.57.1 | LLM & NLP pipelines |
| tokenizers | 0.22.1 | Fast tokenizer engine |
| accelerate | 1.11.0 | Optimized model execution |
| huggingface-hub | 0.36.0 | HF model loading |
| sentencepiece | 0.2.1 | Tokenization backend |
| safetensors | 0.7.0 | Secure tensor format |
| textblob | 0.17.1 | NLP utilities |
| nltk | 3.9.1 | NLP toolkit |

---

## 4️⃣ Computer Vision & Pose Detection

| Package | Version | Purpose |
|---------|---------|---------|
| mediapipe | 0.10.8 | Pose detection engine |
| opencv-contrib-python | 4.8.1.78 | Full OpenCV + extras |
| opencv-python-headless | 4.8.1.78 | OpenCV (no GUI) |

---

## 5️⃣ IoT / MQTT Communication

| Package | Version | Purpose |
|---------|---------|---------|
| paho-mqtt | 2.1.0 | MQTT publisher/subscriber |

---

## 6️⃣ Data Processing & Math Libraries

| Package | Version | Purpose |
|---------|---------|---------|
| numpy | 1.26.4 | Numerical computing |
| pandas | 2.2.2 | DataFrames |
| pyarrow | 22.0.0 | Arrow data format |
| python-dateutil | 2.9.0.post0 | Date helpers |
| pytz | 2025.2 | Timezone handling |
| packaging | 23.2 | Package metadata |

---

## 7️⃣ System Utilities & Helpers

| Package | Version | Purpose |
|---------|---------|---------|
| psutil | 7.1.3 | System monitoring |
| tqdm | 4.67.1 | Progress bars |
| filelock | 3.20.0 | Safe file locking |
| requests | 2.31.0 | HTTP requests |
| urllib3 | 2.5.0 | HTTP client |
| tenacity | 8.5.0 | Retry mechanisms |
| GitPython | 3.1.45 | Git integration |
| gitdb | 4.0.12 | Git DB backend |

---

## 8️⃣ JSON, Schema, & Data Serialization

| Package | Version | Purpose |
|---------|---------|---------|
| PyYAML | 6.0.3 | YAML parsing |
| pydantic | 1.10.13 | Data models & validation |
| jsonschema | 4.25.1 | JSON schema validation |
| jsonschema-specifications | 2025.9.1 | JSON schema specs |
| referencing | 0.37.0 | JSON pointer references |
| rpds-py | 0.29.0 | Rust-based performance utils |

---

## 9️⃣ Parsing, Formatting & Text Utilities

| Package | Version | Purpose |
|---------|---------|---------|
| regex | 2025.11.3 | Advanced regex |
| pyparsing | 3.2.5 | Parsing engine |
| Pygments | 2.19.2 | Syntax highlighting |
| markdown-it-py | 4.0.0 | Markdown parser |
| mdurl | 0.1.2 | URL normalization |
| toml | 0.10.2 | TOML parser |
| tomli | 2.3.0 | TOML loader |

---

## 🔟 Testing Libraries

| Package | Version | Purpose |
|---------|---------|---------|
| pytest | 9.0.1 | Test runner |
| pytest-asyncio | 1.3.0 | Async test support |

---

## 1️⃣1️⃣ Low-Level / Mathematical Libraries

| Package | Version | Purpose |
|---------|---------|---------|
| cffi | 2.0.0 | Foreign function interface |
| pycparser | 2.23 | C parser |
| mpmath | 1.3.0 | Math utilities |
| sympy | 1.14.0 | Symbolic math |

---

## 1️⃣2️⃣ Miscellaneous Support Libraries

| Package | Version | Purpose |
|---------|---------|---------|
| attrs | 25.4.0 | Data classes |
| idna | 3.11 | URL handling |
| charset-normalizer | 3.4.4 | Encoding detection |
| contourpy | 1.3.2 | Plotting helper |
| cycler | 0.12.1 | Color cycles |
| fonttools | 4.60.1 | Font utilities |
| kiwisolver | 1.4.9 | Math solving |
| protobuf | 3.20.3 | Proto serialization |
| MarkupSafe | 3.0.3 | Safe HTML markup |

---

## 1️⃣3️⃣ Optional / Storage & HF Utilities

| Package | Version | Purpose |
|---------|---------|---------|
| flatbuffers | 25.9.23 | Fast binary format |
| hf-xet | 1.2.0 | HF-XET storage backend |
| fsspec | 2025.10.0 | Filesystem interface |

---

## 1️⃣4️⃣ Audio Input Libraries

| Package | Version | Purpose |
|---------|---------|---------|
| sounddevice | 0.5.3 | Microphone audio capture |

---

## 1️⃣5️⃣ Development / Tooling

| Package | Version | Purpose |
|---------|---------|---------|
| setuptools | 80.9.0 | Build utilities |
| pip | 25.3 | Package installer |

---



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
