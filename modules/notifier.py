from dotenv import load_dotenv
from os import environ
import telebot


class Notifier:
    """Sending data to telegram channels"""

    load_dotenv()

    def __init__(self):
        self.bot = telebot.TeleBot(environ.get("BOT_TOKEN"))
        self.chat_id = environ.get("CHAT_ID")

    def send_notification(self, message) -> str:
        return self.bot.send_message(self.chat_id, message, parse_mode="Markdown")
