### Work In progress ###

import json, asyncio, logging, requests
from telegram.error import TelegramError
from ..config import Config
from ..connections import telegram_app
from ._base import Job

logger = logging.getLogger(__name__)

class TelegramPolling(Job):
    def __init__(self, interval: float = 0.5, timeout: float = 3):
        super().__init__(interval=interval, timeout=timeout)
        self.offset = None
        self.webhook_url = str(Config.TELEGRAM_WEBHOOK.load_value())
        self.polling = Config.TELEGRAM_POLLING.load_value()

    def run(self):
        if not self.polling:
            logger.info(f'Telegram Polling is off, stoping the job.')
            self.stop()
            return

        try:
            # Run async get_updates in the current thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            updates = loop.run_until_complete(
                telegram_app.bot.get_updates(offset=self.offset, timeout=5)
            )

            for update in updates:
                self.offset = update.update_id + 1

                # Serialize update exactly as Telegram would send it
                update_json = json.dumps(update.to_dict())

                # Send to Flask webhook endpoint
                resp = requests.post(
                    self.webhook_url,
                    data=update_json,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )

                if resp.status_code != 200:
                    logger.warning(
                        f"Webhook returned {resp.status_code} for update {update.update_id}"
                    )

        except TelegramError as te:
            logger.error(f"Telegram API error: {te}")

        except Exception as e:
            logger.exception(f"Unexpected error in polling job: {e}")
