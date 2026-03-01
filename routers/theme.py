from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram import Bot
from utils.delete_last_message import safe_delete, delete_last_message
from keyboards.theme_kb import levels_kb, themes_kb, subtopic_kb, theory_kb
from states.theory_state import Theory

theme_router = Router()

@theme_router.callback_query(F.data == "theme")
async def theme(call: CallbackQuery, state: FSMContext):
    await safe_delete(call.message)
    bot_msg = await call.message.answer(
        "Выбери свой уровень. Для открытия закрытых тем, пройди предыдущие темы или тест на твой уровень английского",
        reply_markup=levels_kb())
    await state.update_data(last_msg_id=bot_msg.message_id)
    await state.set_state(Theory.level)
    await call.answer()


#выбор уровня
@theme_router.message(Theory.level)
async def level_selection(message: Message, state: FSMContext):
    bot_msg = await message.answer(
        "Пожалуйста, выберите дату с помощью кнопок ниже 👇", reply_markup=levels_kb()
    )
    data = await state.get_data()
    last_msg_id = data.get("last_msg_id")
    await delete_last_message(last_msg_id, message)
    await state.update_data(last_msg_id=bot_msg.message_id)


@theme_router.callback_query(F.data.startswith("level_"))
async def level(call: CallbackQuery, state: FSMContext):
    level_num = call.data.split("_")[1]
    await safe_delete(call.message)
    await state.update_data(level=level_num)
    await call.message.answer("Выбери основную тему:",
                         reply_markup=themes_kb())
    await state.set_state(Theory.theme)
    await call.answer()


#выбор темы
@theme_router.message(Theory.theme)
async def theme_selection(message: Message, state: FSMContext):
    bot_msg = await message.answer(
        "Пожалуйста, выберите дату с помощью кнопок ниже 👇", reply_markup=themes_kb()
    )
    data = await state.get_data()
    last_msg_id = data.get("last_msg_id")
    await delete_last_message(last_msg_id, message)
    await state.update_data(last_msg_id=bot_msg.message_id)


@theme_router.callback_query(F.data.startswith("theme_"))
async def theme(call: CallbackQuery, state: FSMContext):
    theme_num = call.data.split("_")[1]
    await safe_delete(call.message)
    await state.update_data(theme=theme_num)
    await call.message.answer("Выбери подтему:",
                         reply_markup=subtopic_kb())
    await state.set_state(Theory.subtopic)
    await call.answer()

@theme_router.callback_query(F.data == "back_to_levels")
async def back_to_levels(call: CallbackQuery, state: FSMContext):
    await safe_delete(call.message)
    bot_msg = await call.message.answer(
        "Выбери свой уровень. Для открытия закрытых тем, пройди предыдущие темы или тест на твой уровень английского",
        reply_markup=levels_kb())
    await state.update_data(last_msg_id=bot_msg.message_id)
    await state.set_state(Theory.level)
    await call.answer()

#выбор подтемы
@theme_router.message(Theory.subtopic)
async def subtopic_selection(message: Message, state: FSMContext):
    bot_msg = await message.answer(
        "Пожалуйста, выберите дату с помощью кнопок ниже 👇", reply_markup=subtopic_kb()
    )
    data = await state.get_data()
    last_msg_id = data.get("last_msg_id")
    await delete_last_message(last_msg_id, message)
    await state.update_data(last_msg_id=bot_msg.message_id)

@theme_router.callback_query(F.data.startswith("subtopic_"))
async def subtopic(call: CallbackQuery, state: FSMContext):
    subtopic_num = call.data.split("_")[1]
    await safe_delete(call.message)
    await state.update_data(subtopic=subtopic_num)
    await call.message.answer("Описание темы", reply_markup=theory_kb())
    await call.answer()


@theme_router.callback_query(F.data == "back_to_themes")
async def back_to_themes(call: CallbackQuery, state: FSMContext):
    await safe_delete(call.message)
    await call.message.answer("Выбери основную тему:",
                              reply_markup=themes_kb())
    await state.set_state(Theory.theme)
    await call.answer()

@theme_router.callback_query(F.data == "back_to_subtopic")
async def back_to_subtopic(call: CallbackQuery, state: FSMContext):
    await safe_delete(call.message)
    await call.message.answer("Выбери подтему:",
                              reply_markup=subtopic_kb())
    await state.set_state(Theory.subtopic)
    await call.answer()


@theme_router.callback_query(F.data == "learned")
async def learned(call: CallbackQuery, state: FSMContext):
    await call.answer("Тема отмечена выученной")