import asyncio
import logging
from dotenv import load_dotenv
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from commands.command import commands_router, set_bot_commands
from routers.profile import profile_router
from routers.theme import theme_router
from routers.ai_teacher import ai_teacher_router
from routers.tests import tests_router
from routers.my_dictionary import my_dictionary
from routers.payment import payment_router
from database.gspread_db import update_cache

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")

#--ЗАПУСК БОТА--
async def main():
    logger.info("Обновление кеша Google Sheets...")
    await update_cache()
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    main_router = Router()
    dp.include_router(payment_router)
    dp.include_router(commands_router)
    dp.include_router(profile_router)
    dp.include_router(theme_router)
    dp.include_router(ai_teacher_router)
    dp.include_router(tests_router)
    dp.include_router(my_dictionary)
    await set_bot_commands(bot)
    logger.info("Бот запущен и готов к работе!")
    await dp.start_polling(bot, skip_updates=True, allowed_updates=["message", "callback_query", "pre_checkout_query"])

if __name__ == "__main__": #если запускается из этого файла, то работает, если импортируется, то нет
    asyncio.run(main())