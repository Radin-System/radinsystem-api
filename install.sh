#!/bin/bash

APP_DIR="$(cd "$(dirname "$0")"; pwd)"
VENV_DIR="$APP_DIR/.venv"
DIST_DIR="$APP_DIR/dist"
SERVICE_FILE="radin-api.service"
SERVICE_NAME="radin-api"

echo "[*] Creating virtual environment..."
python3 -m venv "$VENV_DIR" || { echo "❌ Failed to create venv"; exit 1; }

echo "[*] Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo "[*] Installing dependencies..."
pip install --upgrade pip
pip install -r "$APP_DIR/requirements.txt" || { echo "❌ Failed to install dependencies"; exit 1; }

echo "[*] Copying systemd service file..."
if [ "$(id -u)" -ne 0 ]; then
    echo "⚠️  Root required to install systemd service. Please enter your password."
    sudo cp "$DIST_DIR/$SERVICE_FILE" "/etc/systemd/system/$SERVICE_FILE" || { echo "❌ Failed to copy service file"; exit 1; }
    sudo systemctl daemon-reload
    sudo systemctl enable "$SERVICE_NAME"
    sudo systemctl start "$SERVICE_NAME"
else
    cp "$DIST_DIR/$SERVICE_FILE" "/etc/systemd/system/$SERVICE_FILE" || { echo "❌ Failed to copy service file"; exit 1; }
    systemctl daemon-reload
    systemctl enable "$SERVICE_NAME"
    systemctl start "$SERVICE_NAME"
fi

echo "[*] Installation complete."
echo "✅ App is now running as a service."
echo "🟢 To run manually:"
echo "$VENV_DIR/bin/gunicorn -w 4 -b 0.0.0.0:8000 app:app"
