import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv

from handlers import (
    set_bot, cmd_start, process_language, process_contact, 
    cmd_appeal, process_appeal_text, process_file_upload, 
    process_file, cmd_my_appeals, Form
)

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

set_bot(bot)

dp.register_message_handler(cmd_start, commands="start", state="*")
dp.register_message_handler(process_language, state=Form.language)
dp.register_message_handler(process_contact, content_types=types.ContentType.CONTACT, state=Form.contact)
dp.register_message_handler(cmd_appeal, Text(equals="Murojat yozish"), state="*")
dp.register_message_handler(process_appeal_text, state=Form.appeal_text)
dp.register_message_handler(process_file_upload, state=Form.file_upload)
dp.register_message_handler(process_file, content_types=types.ContentType.DOCUMENT, state=Form.file_upload)
dp.register_message_handler(cmd_my_appeals, Text(equals="Mening murojatlarim"), state="*")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
