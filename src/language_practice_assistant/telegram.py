import logging
import os
import nest_asyncio

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    filters,
    MessageHandler,
)

logger = logging.getLogger(__name__)

nest_asyncio.apply()

load_dotenv()

TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN")


class TelegramClient:

    def __init__(self, openai_kernel):
        self.application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        self.response_handler = MessageHandler(
            filters.TEXT & (~filters.COMMAND), self.respond
        )
        self.application.add_handler(self.response_handler)
        self.openai_kernel = openai_kernel

    @staticmethod
    async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
        # generic answer that should be given by Semantic Kernel:
        response_text: str = f'Your message was: "{update.message.text}"'

        input_text = update.message.text
        answer = self.openai_kernel.run(input_text=input_text)

        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=response_text
        )

    def run(self):
        self.application.run_polling()
