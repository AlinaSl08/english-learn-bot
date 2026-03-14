from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from utils.delete_last_message import safe_delete, delete_last_message
from keyboards.theme_kb import levels_kb, themes_kb, theory_kb
from states.theory_state import Theory
from database.theme_db import get_topics_and_theory


theme_router = Router()

@theme_router.callback_query(F.data == "theme")
async def theme(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await safe_delete(call.message)
    bot_msg = await call.message.answer(
        "Выбери свой уровень. Для открытия закрытых тем, пройди предыдущие темы или тест на твой уровень английского",
        reply_markup=levels_kb())
    await state.update_data(last_msg_id=bot_msg.message_id)
    await state.set_state(Theory.level)



#выбор уровня
@theme_router.message(Theory.level)
async def level_selection(message: Message, state: FSMContext):
    bot_msg = await message.answer(
        "Пожалуйста, выберите уровень с помощью кнопок ниже 👇", reply_markup=levels_kb()
    )
    data = await state.get_data()
    last_msg_id = data.get("last_msg_id")
    await delete_last_message(last_msg_id, message)
    await state.update_data(last_msg_id=bot_msg.message_id)


@theme_router.callback_query(F.data.startswith("level_"))
async def level(call: CallbackQuery, state: FSMContext):
    await call.answer()
    level_num = int(call.data.split("_")[1])
    await safe_delete(call.message)
    await state.update_data(level=level_num)
    await call.message.answer("Выбери основную тему:",
                         reply_markup=themes_kb(2, level_num, 1))
    await state.set_state(Theory.theme)



#выбор темы
@theme_router.message(Theory.theme)
async def theme_selection(message: Message, state: FSMContext):
    data = await state.get_data()
    level_num = data.get("level")
    bot_msg = await message.answer(
        "Пожалуйста, выберите тему с помощью кнопок ниже 👇",
        reply_markup=themes_kb(2, level_num, 1))
    data = await state.get_data()
    last_msg_id = data.get("last_msg_id")
    await delete_last_message(last_msg_id, message)
    await state.update_data(last_msg_id=bot_msg.message_id)

#следующая тема
@theme_router.callback_query(F.data == "next_theme")
async def next_theme(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await safe_delete(call.message)
    data = await state.get_data()
    level_num = data.get("level")
    await call.message.answer("Выбери основную тему:",
                              reply_markup=themes_kb(2, level_num, 2))



#предыдущая тема
@theme_router.callback_query(F.data == "last_theme")
async def last_theme(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await safe_delete(call.message)
    data = await state.get_data()
    level_num = data.get("level")
    await call.message.answer("Выбери основную тему:",
                              reply_markup=themes_kb(2, level_num, 1))





@theme_router.callback_query(F.data.startswith("theme_"))
async def theme(call: CallbackQuery, state: FSMContext):
    await call.answer()
    theme_num = int(call.data.split("_")[1])
    theme_text = get_topics_and_theory(theme_num)
    await safe_delete(call.message)
    await call.message.answer(theme_text, reply_markup=theory_kb(), parse_mode="HTML")




@theme_router.callback_query(F.data == "back_to_themes")
async def back_to_themes(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await safe_delete(call.message)
    data = await state.get_data()
    level_num = data.get("level")
    await call.message.answer("Выбери основную тему:",
                              reply_markup=themes_kb(2, level_num, 1))
    await state.set_state(Theory.theme)




@theme_router.callback_query(F.data == "learned")
async def learned(call: CallbackQuery, state: FSMContext):
    await call.answer("Тема отмечена выученной")
