#!/bin/bash

# =============================================
#  CONFIGURATION
# =============================================

# Absolute path to uvicorn inside your venv
VENV_PATH="/Users/ksujatha/Projects/ai-gym-and-fitness-asistant/.venv/bin/uvicorn"

# Base project path
BASE_DIR="/Users/ksujatha/Projects/ai-gym-and-fitness-asistant"

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
}

# =============================================
#  BOOT MESSAGE
# =============================================
echo ""
echo "==============================================="
echo "🚀 Starting All AI Fitness Microservices..."
echo "==============================================="

# =============================================
#  START ALL SERVICES
# =============================================

#  folder          port   name                         reload?
start_service "pose-service"   8000 "Pose Detection Service"       YES
start_service "diet-service"   8100 "Diet Planner Service"         YES
start_service "habit-service"  8200 "Habit Tracker Service"        YES

# CHAT SERVICE MUST NOT USE --reload
start_service "chat-service"   8300 "Chat Assistant Service"       NO

start_service "iot-service"    8500 "IoT Smart Gym Service"        YES
start_service "gym-service"    8600 "Gym Recommender Service"      YES

echo ""
echo "==============================================="
echo "🔥 All microservices started successfully!"
echo "==============================================="
echo "🟢 Pose Service:        http://127.0.0.1:8000/health"
echo "🟢 Diet Service:        http://127.0.0.1:8100/health"
echo "🟢 Habit Service:       http://127.0.0.1:8200/health"
echo "🟢 Chat Service:        http://127.0.0.1:8300/health"
echo "🟢 IoT Service:         http://127.0.0.1:8500/health"
echo "🟢 Gym Recommender:     http://127.0.0.1:8600/health"
echo "==============================================="
echo "📌 Run Streamlit UI:"
echo "    streamlit run ai_dashboard/app.py"
echo "==============================================="
