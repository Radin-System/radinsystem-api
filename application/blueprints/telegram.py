### Work in progress ###
# Do not register this in blueprints

from flask import Blueprint, request, jsonify
from telegram import Update
from ..config import Config
from ..connections import telegram_app

telegram_bp = Blueprint('telegram', 'telegram', url_prefix='/telegram')

@telegram_bp.before_app_first_request  # type: ignore
async def update_telegram_webhook():
    await telegram_app.bot.delete_webhook()
    await telegram_app.bot.set_webhook(
        str(Config.TELEGRAM_WEBHOOK.load_value())
    )

# Webhook endpoint
@telegram_bp.route("/webhook", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)

    return jsonify(success=True)
