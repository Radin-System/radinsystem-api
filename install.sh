#!/bin/bash

APP_DIR="$(cd "$(dirname "$0")"; pwd)"
VENV_DIR="$APP_DIR/.venv"
DIST_DIR="$APP_DIR/dist"

echo "[*] Creating virtual environment..."
python3 -m venv "$VENV_DIR" || { echo "❌ Failed to create venv"; exit 1; }

echo "[*] Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo "[*] Installing dependencies..."
pip install --upgrade pip
pip install -r "$APP_DIR/requirements.txt" || { echo "❌ Failed to install dependencies"; exit 1; }

echo "[*] Setting ownership and permissions..."
sudo chown -R radin:radin "$APP_DIR"
sudo chmod -R 755 "$APP_DIR"

echo "[*] Installing all .service files in $DIST_DIR..."
for SERVICE_FILE in "$DIST_DIR"/*.service; do
    [ -e "$SERVICE_FILE" ] || { echo "⚠️ No .service files found."; break; }

    SERVICE_NAME=$(basename "$SERVICE_FILE")
    UNIT_NAME="${SERVICE_NAME%.service}"

    echo "[*] Installing $SERVICE_NAME..."
    if [ "$(id -u)" -ne 0 ]; then
        echo "⚠️ Root required to install systemd service: $SERVICE_NAME"
        sudo cp "$SERVICE_FILE" "/etc/systemd/system/$SERVICE_NAME" || { echo "❌ Failed to copy $SERVICE_NAME"; exit 1; }
        sudo systemctl daemon-reload
        sudo systemctl enable "$UNIT_NAME"
        sudo systemctl start "$UNIT_NAME"
    else
        cp "$SERVICE_FILE" "/etc/systemd/system/$SERVICE_NAME" || { echo "❌ Failed to copy $SERVICE_NAME"; exit 1; }
        systemctl daemon-reload
        systemctl enable "$UNIT_NAME"
        systemctl start "$UNIT_NAME"
    fi
done

echo "[*] Installation complete."
echo "✅ All services from $DIST_DIR are now running."
echo "🟢 To run manually:"
echo "$VENV_DIR/bin/gunicorn -w 4 -b 0.0.0.0:8000 app:app"
