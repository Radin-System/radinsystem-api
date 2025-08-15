import asyncio
import logging
from bs4 import BeautifulSoup
from ..config import Config
from ..api_connections import sarv_client, telegram_bot
from ._base import Job

logger = logging.getLogger(__name__)

CHAT_ID = int(Config.TELEGRAM_CHAT_ID.load_value() or 0)
TICKET_THREAD = int(Config.TELEGRAM_TICKET_THREAD.load_value() or 1)

MESSAGE_TEMPLATE = '''
🎟️ تیکت جدید 🎟️

🔶 عنوان: {name}
💬 توضیحات: {description}
🏢 شرکت: {account_name}
👤 درخواست کننده: {created_by_name}

🖊️ #ticket_{type}
🆔 #ticket_{case_number}
'''

def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()

class SarvCasesToTelegram(Job):
    def run(self) -> None:
        cases = sarv_client.Cases.read_list(
            query="cases.status='New'",
            selected_fields=[
                'id',
                'case_number',
                'name',
                'type',
                'status',
                'description',
                'account_name',
                'created_by_name',
            ],
            limit=2,
            caching=False,
        )

        if not cases:
            logger.debug("No new cases found.")
            return

        for case in cases:
            case_id = case.get("id")
            if not case_id:
                logger.warning("Case without 'id' found, skipping.")
                continue

            try:
                # Prepare message
                message_text = html_to_text(MESSAGE_TEMPLATE.format(**case))

                # Send to Telegram
                telegram_response = asyncio.run(
                    telegram_bot.send_message(
                        chat_id=CHAT_ID,
                        message_thread_id=TICKET_THREAD,
                        text=message_text,
                    )
                )

                if not telegram_response:
                    logger.error(f"No response from Telegram: case.id={case_id}")
                    continue

                # Update SarvCRM
                sarv_response = None
                try:
                    sarv_response = sarv_client.Cases.update(case_id, status="Pending")

                except Exception as e:
                    logger.error(f"Error while updating case: id={case_id} - {repr(e)}")

                finally :
                    if not sarv_response:
                        logger.error(f"No response from sarvcrm, removing telegram message.")

                        asyncio.run(
                            telegram_bot.delete_message(
                                chat_id=CHAT_ID,
                                message_id=telegram_response.message_id
                            )
                        )
                        logger.info(f"Deleted Telegram message for failed Sarv update: case.id={case_id}")

            except Exception as e:
                logger.exception(f"Unexpected error processing case.id={case_id}: {repr(e)}")
