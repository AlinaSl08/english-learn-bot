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

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

#--ЗАПУСК БОТА--
async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    logging.basicConfig(level=logging.INFO)

    main_router = Router()
    dp.include_router(commands_router)
    dp.include_router(profile_router)
    dp.include_router(theme_router)
    dp.include_router(ai_teacher_router)
    dp.include_router(tests_router)
    dp.include_router(my_dictionary)
    await set_bot_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__": #если запускается из этого файла, то работает, если импортируется, то нет
    asyncio.run(main())