from aiogram.utils.keyboard import InlineKeyboardBuilder


def questions_kb(): #сделать замочки если нет премиум
    kb = InlineKeyboardBuilder()
    for i in range(1, 5):
        kb.button(text=f'Вопрос {i}', callback_data=f'question_{i}')
    kb.button(text='⬅️ Назад', callback_data='back_to_theme_test')
    count = 5
    if count <= 4:
        kb.adjust(1)
    elif count <= 10:
        kb.adjust(2)
    else:
        kb.adjust(3)
    return kb.as_markup()


def answers_kb():
    kb = InlineKeyboardBuilder()
    for i in range(1, 5):
        kb.button(text=f'Вариант {i}', callback_data=f'answer_{i}')
    kb.button(text='⬅️ Назад', callback_data='back_to_questions_test')
    count = 5
    if count <= 4:
        kb.adjust(1)
    elif count <= 10:
        kb.adjust(2)
    else:
        kb.adjust(3)
    return kb.as_markup()



