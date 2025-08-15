from telegram import Bot
from telegram.request import HTTPXRequest
from ..config import Config


telegram_bot = Bot(
    token=str(Config.TELEGRAM_TOKEN.load_value()),
    request=HTTPXRequest(connection_pool_size=50, pool_timeout=10),
)
