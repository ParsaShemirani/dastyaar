#!/bin/bash

# Remote server setup script
# Connects to remote server and starts the dastyaar console server in tmux

set -e  # Exit on any error

SERVER_USER="parsa"
SERVER_IP="192.168.1.4"
PROJECT_DIR="~/dastyaar"
TMUX_SESSION="console_server"
VENV_PATH="venv/bin/activate"
GUNICORN_CMD="gunicorn -w 2 -b 0.0.0.0:8321 server.console:app"

echo "🚀 Connecting to ${SERVER_USER}@${SERVER_IP} and setting up console server..."

# SSH into the remote server and execute the commands
ssh "${SERVER_USER}@${SERVER_IP}" << EOF
    echo "📁 Navigating to project directory: ${PROJECT_DIR}"
    cd ${PROJECT_DIR}
    
    echo "🔪 Killing existing gunicorn processes..."
    pkill -f "gunicorn.*server.console:app" 2>/dev/null || true
    sleep 1
    echo "✅ Gunicorn processes cleaned up"
    
    echo "🔪 Killing existing tmux sessions..."
    tmux kill-server 2>/dev/null || true
    echo "✅ Tmux server cleaned up"
    
    echo "🔍 Verifying port 8321 is free..."
    if lsof -i :8321 >/dev/null 2>&1; then
        echo "⚠️  Port 8321 still in use, force killing processes..."
        lsof -ti :8321 | xargs kill -9 2>/dev/null || true
        sleep 1
        if lsof -i :8321 >/dev/null 2>&1; then
            echo "❌ Unable to free port 8321, exiting..."
            exit 1
        fi
    fi
    echo "✅ Port 8321 is now available"
    
    echo "🆕 Creating new tmux session: ${TMUX_SESSION}"
    tmux new-session -d -s "${TMUX_SESSION}"
    echo "✅ Tmux session '${TMUX_SESSION}' created"
    
    echo "🐍 Activating virtual environment..."
    tmux send-keys -t "${TMUX_SESSION}" "cd ${PROJECT_DIR}" Enter
    tmux send-keys -t "${TMUX_SESSION}" "source ${VENV_PATH}" Enter
    sleep 1
    echo "✅ Virtual environment activated"
    
    echo "🦄 Starting Gunicorn server..."
    tmux send-keys -t "${TMUX_SESSION}" "${GUNICORN_CMD}" Enter
    sleep 2
    echo "✅ Gunicorn command sent to tmux session"
    
    echo "🔍 Checking if tmux session is running..."
    if tmux has-session -t "${TMUX_SESSION}" 2>/dev/null; then
        echo "✅ Tmux session '${TMUX_SESSION}' is active"
    else
        echo "❌ Warning: Tmux session may not be running properly"
        exit 1
    fi
    
    echo "🔍 Checking if port 8321 is in use..."
    if lsof -i :8321 >/dev/null 2>&1; then
        echo "✅ Port 8321 is active - server appears to be running!"
    else
        echo "⚠️  Port 8321 not detected yet (may still be starting up)"
    fi
    
    echo ""
    echo "📋 Setup Summary:"
    echo "  • Project directory: ${PROJECT_DIR}"
    echo "  • Tmux session: ${TMUX_SESSION}"
    echo "  • Server address: ${SERVER_IP}:8321"
    echo "  • To attach later: tmux attach -t ${TMUX_SESSION}"
EOF

echo ""
echo "🎉 Setup complete! Console server deployment finished."
echo "🌐 Your server should be accessible at: http://${SERVER_IP}:8321"
echo "🔗 To connect to tmux session: ssh ${SERVER_USER}@${SERVER_IP} -t 'tmux attach -t ${TMUX_SESSION}'"
echo "📊 To check server status: ssh ${SERVER_USER}@${SERVER_IP} 'tmux list-sessions'"