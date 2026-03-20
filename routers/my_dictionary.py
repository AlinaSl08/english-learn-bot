from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from utils.delete_last_message import safe_delete, delete_last_message
from keyboards.my_dictionary_kb import words_topic_kb
from database.gspread_db import get_words_and_card_words


my_dictionary = Router()

@my_dictionary.callback_query(F.data == "my_dictionary")
async def show_my_dictionary(call: CallbackQuery, state: FSMContext):
    # потом поменять на sql
    words_count = 1
    if words_count == 0:
        #bot_msg = await call.message.answer(
            #"У вас еще нет сохраненных слов. Вы можете ознакомиться со списком слов тут: тут ссылка ")
        await call.answer('Команда в разработке. Пожалуйста, нажмите меню', show_alert=True)
        #await state.update_data(last_msg_id=bot_msg.message_id)
        return
    await call.answer() #потом в начало переместить
    await safe_delete(call.message) #потом в начало переместить

    bot_msg = await call.message.answer(
        f"Всего сохраненных слов: {words_count}.\n\nВы можете просмотреть заново карточки слов, которые ранее сохранили.\n\nВыберите тему:",
        reply_markup=words_topic_kb())
    await state.update_data(last_msg_id=bot_msg.message_id)




@my_dictionary.callback_query(F.data.startswith("topic_"))
async def words_list(call: CallbackQuery, state: FSMContext):
    topic = int(call.data.split("_")[1])
    await safe_delete(call.message)
    await state.update_data(topic=topic)
    # потом по айди темы ищет слова
    await call.answer('Команда в разработке. Пожалуйста, нажмите меню')
