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

    await set_bot_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__": #если запускается из этого файла, то работает, если импортируется, то нет
    asyncio.run(main())