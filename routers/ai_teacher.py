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


load_dotenv()
GIGA_TOKEN = os.getenv("GIGACHAT_API_KEY")

giga = GigaChat(credentials=GIGA_TOKEN, verify_ssl_certs=False)

# Инициализация списка для хранения сообщений
messages = []


ai_teacher_router = Router()

#промт на общий чат
def create_general_prompt(user_input):
    return (f"Ты — помощник по изучению английского языка. "
            f"Пользователь будет задавать вопросы, и ты должен отвечать на них, "
            f"если они касаются изучения английского языка. Если пользователь "
            f"задает вопрос, не относящийся к теме, вежливо перенаправь его на "
            f"вопросы по английскому языку. "
            f"Пользователь спросил: \"{user_input}\"")



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
    bot_msg = await call.message.answer(
        "Количество запросов на сегодня: 10\nБот будет объяснять темы, которые касаются вашего уровня.\n"
        "Вы можете обсудить с ИИ-ассистентом определенную тему или открыть общий чат",
        reply_markup=ai_themes_kb())
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
    await state.set_state("general_chat")
    print("Пользователь выбрал общий чат")
    await call.answer()


# Обработчик текстовых сообщений в общем чате
@ai_teacher_router.message(F.text, StateFilter("general_chat"))
async def handle_general_chat_message(message: Message, state: FSMContext):
    user_input = message.text
    data = await state.get_data()
    user_history = data.get("messages", [])

    # Проверка на выход
    if user_input.lower() == "выход":
        await message.answer("Вы вышли из чата.")
        await state.clear()
        bot_msg = await message.answer("Выберите действие:", reply_markup=menu_kb())
        await state.update_data(last_msg_id=bot_msg.message_id)  # Сохраняем ID последнего сообщения
        return

    prompt = create_general_prompt(user_input)
    user_history.append({"role": "user", "content": prompt})
    try:
        ai_response = await get_ai_response(user_history)
        user_history.append({"role": "assistant", "content": ai_response})
        await state.update_data(messages=user_history)
        await message.answer(ai_response)
    except Exception as e:
        await message.answer("Произошла ошибка при обращении к GigaChat.")
        print(f"Ошибка: {e}")
