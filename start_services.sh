#!/bin/bash

# =============================================
#  CONFIGURATION
# =============================================

# Absolute path to uvicorn inside your venv
VENV_PATH="/Users/ksujatha/Projects/ai-gym-and-fitness-asistant/.venv/bin/uvicorn"

# Base project path
BASE_DIR="/Users/ksujatha/Projects/ai-gym-and-fitness-asistant"

# Path to Streamlit inside venv
STREAMLIT_PATH="/Users/ksujatha/Projects/ai-gym-and-fitness-asistant/.venv/bin/streamlit"

# Mosquitto config
MOSQUITTO_CONF="/usr/local/etc/mosquitto/mosquitto.conf"

# =============================================
#  UTILITY: KILL PORT IF OCCUPIED
# =============================================
kill_port() {
    PORT=$1
    PID=$(lsof -ti tcp:$PORT)

    if [ -n "$PID" ]; then
        echo "⚠️  Port $PORT is busy (PID $PID). Killing..."
        kill -9 $PID
        sleep 1
        echo "✅ Port $PORT is free now."
    else
        echo "🟢 Port $PORT is free."
    fi
}

# =============================================
#  UTILITY: START SERVICE
# =============================================
start_service() {
    local folder=$1
    local port=$2
    local name=$3
    local reload_flag=$4   # YES or NO

    echo ""
    echo "--------------------------------------------------"
    echo "▶️ Starting $name (Folder: $folder) on port $port"
    echo "--------------------------------------------------"

    kill_port "$port"
    cd "$BASE_DIR/ai-services/$folder" || exit

    if [ "$reload_flag" == "NO" ]; then
        echo "⚡ Starting WITHOUT reload (stable mode)"
        $VENV_PATH app.main:app --port "$port" &
    else
        echo "🔄 Starting WITH reload (dev mode)"
        $VENV_PATH app.main:app --reload --port "$port" &
    fi

    sleep 1
    echo "✅ $name started on port $port"

    cd "$BASE_DIR"
}

# =============================================
#  BOOT MESSAGE
# =============================================
echo ""
echo "==============================================="
echo "🚀 Starting Mosquitto, Microservices & Streamlit"
echo "==============================================="

# =============================================
#  MOSQUITTO
# =============================================
echo ""
echo "--------------------------------------------------"
echo "🔌 Stopping Mosquitto if running..."
echo "--------------------------------------------------"
pkill -f mosquitto 2>/dev/null || true
sleep 1

echo "--------------------------------------------------"
echo "🚀 Starting Mosquitto MQTT Broker"
echo "--------------------------------------------------"
mosquitto -c "$MOSQUITTO_CONF" &
sleep 1
echo "🟢 Mosquitto Started"

# =============================================
#  START ALL MICROSERVICES
# =============================================

start_service "pose-service"   8000 "Pose Detection Service"       YES
start_service "diet-service"   8100 "Diet Planner Service"         YES
start_service "habit-service"  8200 "Habit Tracker Service"        YES
start_service "chat-service"   8300 "Chat Assistant Service"       NO
start_service "iot-service"    8500 "IoT Smart Gym Service"        YES
start_service "gym-service"    8600 "Gym Recommender Service"      YES

# =============================================
#  START STREAMSIT IN FOREGROUND (OPTION A)
# =============================================

echo ""
echo "--------------------------------------------------"
echo "📺 Starting Streamlit UI (foreground mode)"
echo "--------------------------------------------------"

cd "$BASE_DIR"

# Running in FOREGROUND so browser opens
PYTHONPATH=$(pwd) $STREAMLIT_PATH run ai_dashboard/Home.py

# Script will block here — other services continue running in background

