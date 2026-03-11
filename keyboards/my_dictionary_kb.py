from aiogram.utils.keyboard import InlineKeyboardBuilder

def words_topic_kb():
    kb = InlineKeyboardBuilder()
    topics_list = {1: 'Приветствия и базовые слова', 2: 'Люди и семья', 3: 'Еда и напитки',
                   4: 'Места', 5: 'Время', 6: 'Глаголы', 7: 'Транспорт и путешествия',
                   8: 'Тело и здоровье', 9: 'Прилагательные', 10: 'Предметы'}
    for key, topic in topics_list.items():
        kb.button(text=topic, callback_data=f'topic_{key}') #потом выводить Тема: кол-во сохраненных
    kb.button(text='⬅️ Назад', callback_data='cancel_menu')
    kb.adjust(2, 2, 2, 2, 2, 1)
    return kb.as_markup()

