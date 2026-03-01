from aiogram.utils.keyboard import InlineKeyboardBuilder


def levels_kb():
    kb = InlineKeyboardBuilder()
    for i in range(1, 5):
        kb.button(text=f'Уровень {i}', callback_data=f'level_{i}')
    kb.button(text='⬅️ Назад', callback_data='cancel_menu')
    kb.button(text='Сдать тест на уровень', callback_data='test_level')
    count = 5
    if count <= 4:
        kb.adjust(1)
    elif count <= 10:
        kb.adjust(2)
    else:
        kb.adjust(3)
    return kb.as_markup()

def themes_kb(mode_key=1):
    kb = InlineKeyboardBuilder()
    modes = {1: 'test', 2: 'theory'}
    mode = modes[mode_key]
    if mode == 'theory': #тут добавить проставление галочек
        for i in range(1, 5):
            kb.button(text=f'Тема {i}', callback_data=f'theme_{i}')
        kb.button(text='⬅️ Назад', callback_data='theme')
    else: #тут добавить проставление галочек
        for i in range(1, 5):
            kb.button(text=f'Тема {i}', callback_data=f'test_theme_{i}')
        kb.button(text='⬅️ Назад', callback_data='tests')
    count = 5
    if count <= 4:
        kb.adjust(1)
    elif count <= 10:
        kb.adjust(2)
    else:
        kb.adjust(3)
    return kb.as_markup()

def subtopic_kb():
    kb = InlineKeyboardBuilder()
    for i in range(1, 5):
        kb.button(text=f'Подтема {i}', callback_data=f'subtopic_{i}')
    kb.button(text='⬅️ Назад', callback_data='back_to_themes')
    count = 5
    if count <= 4:
        kb.adjust(1)
    elif count <= 10:
        kb.adjust(2)
    else:
        kb.adjust(3)
    return kb.as_markup()

def theory_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='✅ Выучено', callback_data='learned') #сделать изначально без галки, при нажатии чтобы была галка
    kb.button(text='⬅️ Назад', callback_data='back_to_subtopic')
    kb.button(text='📝 Перейти к тестам', callback_data='go_to_tests') #в разработке
    kb.button(text='⬅️ Вернуться в меню', callback_data='cancel_menu')
    kb.adjust(2, 2)
    return kb.as_markup()
