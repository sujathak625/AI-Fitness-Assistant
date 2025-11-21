# 🏋️ AI Gym & Fitness Assistant

A complete **microservices-based fitness platform** featuring AI pose detection, diet planning, IoT integration, habit tracking, and a unified Streamlit dashboard.

This project follows a **Microservices Architecture** with multiple **FastAPI** backend services connected to a central **Streamlit** UI.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)  
- [Prerequisites](#️-prerequisites)  
- [Installation](#-installation)  
- [Project Structure](#-project-structure)  
- [How to Run](#-how-to-run-step-by-step)  
- [Features & Testing](#-features--testing)  
- [Configuration](#-configuration)

---

## 🌟 Project Overview

The platform includes the following components:

| Module | Description |
|--------|-------------|
| 🏋️ **AI Workout Pose Detector** | Real-time AI-based pose detection |
| 🥗 **AI Diet Planner** | Personalized meal plans using LLMs |
| 💬 **AI Chat Assistant** | Fitness + general chat assistant |
| 📊 **Habit Tracker** | Track and view daily habits |
| 🚴 **IoT Smart Gym Dashboard** | Live gym equipment telemetry via MQTT |
| 🏢 **Gym Recommendation Service** | Find gyms based on location + budget |
| 🎛️ **Streamlit Dashboard** | Unified UI |

---

## ⚙️ Prerequisites

### System Requirements

- **Python 3.10+**  
- **macOS / Linux / Windows**

### Mosquitto MQTT Broker (Required for IoT)

| OS | Installation |
|----|--------------|
| macOS | `brew install mosquitto` |
| Linux | `sudo apt install mosquitto` |
| Windows | Download installer from Mosquitto website |

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ai-gym-and-fitness-assistant
```

---

### 2. Create Virtual Environment

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Key Dependencies

| Purpose | Libraries |
|---------|-----------|
| Backend API | `fastapi`, `uvicorn` |
| Frontend | `streamlit`, `pandas`, `plotly` |
| AI Pose Detection | `mediapipe`, `opencv-python` |
| IoT MQTT | `paho-mqtt` |

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

You need **3 terminals** to run the system.

---

### 🖥️ Terminal 1 — Start MQTT Broker

```bash
mosquitto
```

---

### 🖥️ Terminal 2 — Start All Backend Services

```bash
chmod +x start-services.sh
./start-services.sh
```

---

### 🖥️ Terminal 3 — Start Streamlit UI

```bash
cd ai_dashboard
streamlit run app.py
```

Access the dashboard at:  
👉 **http://localhost:8501**

---

## 🧪 Features & Testing

| Feature | How to Test |
|---------|-------------|
| 🥗 Diet Planner | Chat Assistant → “I need a diet plan” |
| 🚴 IoT Dashboard | IoT Page → Select machine → Start Streaming |
| 🏢 Gym Finder | Chat Assistant → “Find gyms under 2000 in Bangalore” |
| 📊 Habit Tracker | Add habits → View logs + summary |
| 🏋️ Pose Detector | Allow camera → Perform a workout |

---

## 🔧 Configuration

Update backend service URLs:

### `ai_dashboard/config.py`

```python
POSE_SERVICE_URL = "http://127.0.0.1:8000"
DIET_SERVICE_URL = "http://127.0.0.1:8100"
HABIT_SERVICE_URL = "http://127.0.0.1:8200"
CHAT_SERVICE_URL = "http://127.0.0.1:8300"
IOT_SERVICE_URL = "http://127.0.0.1:8500"
GYM_SERVICE_URL = "http://127.0.0.1:8600"
```

---

