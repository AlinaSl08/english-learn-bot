from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.filters import StateFilter
from utils.delete_last_message import safe_delete, delete_last_message
from keyboards.ai_teacher_kb import ai_themes_kb
from keyboards.menu_kb import menu_kb
from gigachat import GigaChat
from dotenv import load_dotenv
import os
from gigachat.models import Chat
from states.menu_state import Menu


load_dotenv()
GIGA_TOKEN = os.getenv("GIGACHAT_API_KEY")

giga = GigaChat(credentials=GIGA_TOKEN, verify_ssl_certs=False)
ai_teacher_router = Router()


async def get_ai_response(history_list):
    payload = Chat(
        messages=history_list,
        model="GigaChat"
    )
    response = await giga.achat(payload)
    return response.choices[0].message.content


@ai_teacher_router.callback_query(F.data == "ai_teacher")
async def ai_teacher(call: CallbackQuery, state: FSMContext):
    await safe_delete(call.message)
    token = 10
    bot_msg = await call.message.answer(
        f"🎓 *Ваш персональный ИИ-наставник готов к работе!*\n\n"
        f"📊 *Доступно запросов на сегодня:* `{token}`\n\n"
        "Я помогу вам разобраться в сложных темах, учитывая ваш текущий уровень знаний. "
        "Мы можем сфокусироваться на конкретном модуле или пообщаться в свободном режиме.\n\n"
        "👇 *Выберите формат обучения:*",
        reply_markup=ai_themes_kb(), parse_mode="Markdown")
    await state.update_data(last_msg_id=bot_msg.message_id)
    await call.answer()

#чат по теме
@ai_teacher_router.callback_query(F.data.startswith("ai_theme_"))
async def ai_theme(call: CallbackQuery, state: FSMContext):
    await safe_delete(call.message)
    theme = int(call.data.split("_")[2])
    await call.message.answer(f"Вы выбрали тему: {theme}. Напишите сообщение боту по выбранной теме")
    bot_msg = await call.message.answer("Выберите действие:", reply_markup=menu_kb())
    await state.update_data(last_msg_id=bot_msg.message_id)
    await call.answer()

#общий чат
@ai_teacher_router.callback_query(F.data == "general_chat")
async def general_chat(call: CallbackQuery, state: FSMContext):
    await safe_delete(call.message)
    await call.message.answer("Вы выбрали общий чат. Напишите сообщение боту. Для завершения общения, напишите слово: «Выход»")
    await state.update_data(messages=[{
            "role": "system",
            "content": (
                "Ты — помощник по изучению английского языка. "
            f"Пользователь будет задавать вопросы, и ты должен отвечать на них, "
            f"если они касаются изучения английского языка. Если пользователь "
            f"задает вопрос, не относящийся к теме, вежливо перенаправь его на "
            f"вопросы по английскому языку.")}])
    await state.set_state("general_chat")
    await call.answer()


# Обработчик текстовых сообщений в общем чате
@ai_teacher_router.message(F.text & ~F.text.startswith("/"), StateFilter("general_chat"))
async def handle_general_chat_message(message: Message, state: FSMContext):
    user_input = message.text
    data = await state.get_data()
    user_history = data.get("messages", [])

    # Проверка на выход
    if user_input.lower() == "выход":
        await message.answer("Вы вышли из чата. Ждем вас снова 👋")
        await state.clear()
        bot_msg = await message.answer("Выберите действие:", reply_markup=menu_kb())
        await state.update_data(last_msg_id=bot_msg.message_id)  # Сохраняем ID последнего сообщения
        await state.set_state(Menu.menu)
        return

    user_history.append({
        "role": "user",
        "content": user_input
    })

    try:
        ai_response = await get_ai_response(user_history)
        user_history.append({"role": "assistant", "content": ai_response})
        await state.update_data(messages=user_history)
        await message.answer(ai_response)
    except Exception as e:
        await message.answer("Произошла ошибка при обращении к GigaChat.")
        print(f"Ошибка: {e}")
