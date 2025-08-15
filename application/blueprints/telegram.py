### Work In progress ###

import ipaddress
from flask import Blueprint, request, jsonify, abort
from telegram import Update
from ..config import Config
from ..connections import telegram_app


telegram_bp = Blueprint('telegram', 'telegram', url_prefix='/telegram')


async def update_telegram_webhook():
    if Config.TELEGRAM_POLLING.load_value():
        await telegram_app.bot.delete_webhook()

    else:
        await telegram_app.bot.set_webhook(
            str(Config.TELEGRAM_WEBHOOK.load_value())
        )

TELEGRAM_NETWORKS = [
    ipaddress.ip_network(net) for net in [
        "127.0.0.0/8",
        "149.154.160.0/20",
        "91.108.4.0/22",
    ]
]

def is_telegram_ip(ip: str) -> bool:
    try:
        ip_obj = ipaddress.ip_address(ip)
        return any(ip_obj in net for net in TELEGRAM_NETWORKS)
    except ValueError:
        return False

@telegram_bp.route("/webhook", methods=["POST"])
async def webhook():
    # Get the client IP
    client_ip = request.headers.get('X-Real-IP', request.remote_addr)

    if not client_ip or not is_telegram_ip(client_ip):
        # Reject requests not from Telegram
        return abort(403, description="Forbidden: IP not allowed")

    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)

    return jsonify(success=True)