from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from utils.delete_last_message import safe_delete, delete_last_message
from keyboards.ai_teacher_kb import ai_themes_kb
from keyboards.menu_kb import menu_kb


ai_teacher_router = Router()

@ai_teacher_router.callback_query(F.data == "ai_teacher")
async def ai_teacher(call: CallbackQuery, state: FSMContext):
    await safe_delete(call.message)
    bot_msg = await call.message.answer(
        "Количество запросов на сегодня: 10\nБот будет объяснять темы, которые касаются вашего уровня.\n"
        "Вы можете обсудить с ИИ-ассистентом определенную тему или открыть общий чат",
        reply_markup=ai_themes_kb())
    await state.update_data(last_msg_id=bot_msg.message_id)
    await call.answer()


@ai_teacher_router.callback_query(F.data.startswith("ai_theme_"))
async def ai_theme(call: CallbackQuery, state: FSMContext):
    await safe_delete(call.message)
    theme = int(call.data.split("_")[2])
    await call.message.answer(f"Вы выбрали тему: {theme}. Напишите сообщение боту по выбранной теме")
    bot_msg = await call.message.answer("Выберите действие:", reply_markup=menu_kb())
    await state.update_data(last_msg_id=bot_msg.message_id)
    await call.answer()

@ai_teacher_router.callback_query(F.data == "general_chat")
async def general_chat(call: CallbackQuery, state: FSMContext):
    await safe_delete(call.message)
    await call.message.answer("Вы выбрали общий чат. Напишите сообщение боту")
    bot_msg = await call.message.answer("Выберите действие:", reply_markup=menu_kb())
    await state.update_data(last_msg_id=bot_msg.message_id)
    await call.answer()


