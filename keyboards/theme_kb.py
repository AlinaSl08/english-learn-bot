from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.theme_db import get_topics_and_theory

def levels_kb():
    kb = InlineKeyboardBuilder()
    levels = ['Уровень A1', 'Уровень A2', 'Уровень B1', 'Уровень B2']
    for i in range(1, 5):
        kb.button(text=f'Уровень {levels[i - 1]}', callback_data=f'level_{i}')
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

def themes_kb(mode_key=1, level=1, page=1):
    kb = InlineKeyboardBuilder()
    modes = {1: 'test', 2: 'theory'}
    mode = modes[mode_key]
    if page == 1:
        levels = {1: [0, 7], 2: [16, 23], 3: [30, 37], 4: [43, 48]}
    else:
        levels = {1: [7, 15], 2: [23, 29], 3: [37, 42], 4: [48, 52]}
    for i in range(levels[level][0], levels[level][1]):
        topic  = get_topics_and_theory(i)[1]
        if mode == 'theory': #тут добавить проставление галочек(если в sql не 0, то галка есть)
            kb.button(text=topic, callback_data=f'theme_{i}')
        else: #тут добавить проставление галочек(если в sql не 0, то галка есть)
            kb.button(text=topic, callback_data=f'test_theme_{i}')
    if page == 1:
        #kb.button(text=' ', callback_data='cap')
        kb.button(text='>', callback_data='next_theme')
    else:
        kb.button(text='<', callback_data='last_theme')
        #kb.button(text=' ', callback_data='cap')
    if mode == 'theory':
        kb.button(text='⬅️ Назад', callback_data='theme')
    else:
        kb.button(text='⬅️ Назад', callback_data='tests')
    kb.adjust(1)
    return kb.as_markup()



def theory_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='✅ Выучено', callback_data='learned') #сделать изначально без галки, при нажатии чтобы была галка, (если в sql есть, то галка, если нет то вернет null)
    kb.button(text='⬅️ Назад', callback_data='back_to_themes')
    kb.button(text='📝 Перейти к тестам', callback_data='go_to_tests') #сделать переход к тестам по определенной теме
    kb.button(text='⬅️ Вернуться в меню', callback_data='cancel_menu')
    kb.adjust(2, 2)
    return kb.as_markup()
