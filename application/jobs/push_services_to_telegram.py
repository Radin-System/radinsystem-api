import asyncio
from bs4 import BeautifulSoup
from ..config import Config
from ..api_connections import sarv_client, telegram_bot
from ._base import Job

CHAT_ID = int(Config.TELEGRAM_CHAT_ID.load_value() or 0)
TICKET_THREAD = int(Config.TELEGRAM_TICKET_THREAD.load_value() or 1)

MESSAGE_TEMPLATE = '''
🎟️ تیکت جدید 🎟️

🔶 عنوان: {name}
💬 توضیحات: {description}
🏢 شرکت: {account_name}
👤 کاربر: {created_by_name}

🖊️ #ticket_{type}
🆔 #ticket_{case_number}
'''

def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()


class PushServicesToTelegram(Job):
    def run(self) -> None:
        async def send_telegram_message(text):
            return await telegram_bot.send_message(
                chat_id=CHAT_ID,
                message_thread_id=TICKET_THREAD,
                text=text,
            )
        with sarv_client:
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
                limit=3,
            )
            if not cases: return

            for case in cases:
                case_id = case.get('id')
                if not case_id: 
                    continue

                message = html_to_text(MESSAGE_TEMPLATE.format(**case))

                response = asyncio.run(
                    send_telegram_message(message)
                )

                if response:
                    sarv_client.Cases.update(case_id, status='Pending')

                else:
                    raise TimeoutError('No Response from telegram server')
