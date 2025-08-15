from telegram.ext import ApplicationBuilder
from telegram.request import HTTPXRequest
from ..config import Config


telegram_app = ApplicationBuilder(
).token(
    str(Config.TELEGRAM_TOKEN.load_value()),
).request(
    HTTPXRequest(connection_pool_size=50, pool_timeout=10),
).build()