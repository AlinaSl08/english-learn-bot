from aiogram.utils.keyboard import InlineKeyboardBuilder

def words_topic_kb():
    kb = InlineKeyboardBuilder()
    topics_list = {1: 'Основы', 2: 'Семья и люди', 3: 'Еда и напитки',
                   4: 'Места и дом', 5: 'Время и числа', 6: 'Основные глаголы',
                   7: 'Транспорт', 8: 'Тело и здоровье', 9: 'Описания', 10: 'Вещи'}
    for key, topic in topics_list.items():
        kb.button(text=topic, callback_data=f'topic_{key}') #потом выводить Тема: кол-во сохраненных
    kb.button(text='⬅️ Назад', callback_data='cancel_menu')
    kb.adjust(2, 2, 2, 2, 2, 1)
    return kb.as_markup()

