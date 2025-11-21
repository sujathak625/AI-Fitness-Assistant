🏋️ AI Gym & Fitness Assistant

A complete microservices-based fitness platform featuring AI pose detection, diet planning, IoT integration, habit tracking, and a unified Streamlit dashboard.

This project uses a Microservices Architecture where individual FastAPI services communicate with a central Streamlit UI.

📋 Table of Contents

Project Overview

Prerequisites

Installation

Project Structure

🚀 How to Run (Step-by-Step)

Features & Testing

Configuration

🌟 Project Overview

The platform includes the following modules:

Module	Description
🏋️ AI Workout Pose Detector	Real-time workout pose detection & feedback
🥗 AI Diet Planner	Personalized diet generation using LLM
💬 AI Chat Assistant	Fitness & general query handling
📊 Habit Tracker	Add + view daily habit logs
🚴 IoT Smart Gym Dashboard	Displays MQTT telemetry from gym equipment
🏢 Gym Recommendation Service	Suggests gyms based on location & budget
🎛️ Unified Streamlit UI	Full frontend dashboard
⚙️ Prerequisites
System Requirements

Python: 3.10+

OS: macOS / Linux / Windows

Mosquitto MQTT Broker

Required for IoT service.

OS	Installation
macOS	brew install mosquitto
Linux	sudo apt install mosquitto
Windows	Download installer from Mosquitto website
📦 Installation
1. Clone the Repository
git clone <your-repo-url>
cd ai-gym-and-fitness-assistant

2. Create Virtual Environment

Since the ZIP won’t include .venv, create a new environment.

macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate

Windows:
python -m venv .venv
.venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

Key Dependencies
Category	Packages
Backend	fastapi, uvicorn
Frontend	streamlit, plotly, pandas
Computer Vision	opencv-python, mediapipe
IoT	paho-mqtt
📂 Project Structure
ai-gym-and-fitness-assistant/
│
├── start-services.sh            # Start all backend microservices
│
├── ai_dashboard/                # Streamlit UI
│   ├── app.py                   # Main dashboard launcher
│   ├── config.py                # Backend service URLs
│   └── pages/                   # Individual UI pages
│
└── ai-services/                 # FastAPI microservices
    ├── pose-service/
    ├── diet-service/
    ├── habit-service/
    ├── chat-service/
    ├── iot-service/
    └── gym-service/

🚀 How to Run (Step-by-Step)

You need three terminals to run the full stack.

🖥️ Terminal 1 — Start MQTT Broker
mosquitto

🖥️ Terminal 2 — Start All Backend Services

From project root:

chmod +x start-services.sh
./start-services.sh


This launches all 6 FastAPI microservices.

🖥️ Terminal 3 — Start Streamlit Frontend
cd ai_dashboard
streamlit run app.py


Then open:

👉 http://localhost:8501

🧪 Features & Testing
Feature	How to Test
🥗 Diet Planner	Chat Assistant → “I need a diet plan”
🚴 IoT Dashboard	IoT Page → Select machine → Start Streaming
🏢 Gym Finder	Chat Assistant → “Find me gyms in Bangalore under 2000”
📊 Habit Tracker	Add habits → View logs & summary
🏋️ Pose Detector	Open Pose Detector → Allow camera → Perform exercise
🔧 Configuration

Modify backend service URLs in:

ai_dashboard/config.py
POSE_SERVICE_URL = "http://127.0.0.1:8000"
DIET_SERVICE_URL = "http://127.0.0.1:8100"
HABIT_SERVICE_URL = "http://127.0.0.1:8200"
CHAT_SERVICE_URL = "http://127.0.0.1:8300"
IOT_SERVICE_URL = "http://127.0.0.1:8500"
GYM_SERVICE_URL = "http://127.0.0.1:8600"
