from telegram import Bot
from ..config import Config

telegram_bot = Bot(
    token=str(Config.TELEGRAM_TOKEN.load_value()),
)