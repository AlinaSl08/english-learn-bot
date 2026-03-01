from aiogram.utils.keyboard import InlineKeyboardBuilder

def ai_themes_kb():
    kb = InlineKeyboardBuilder()
    for i in range(1, 5):
        kb.button(text=f'Тема {i}', callback_data=f'ai_theme_{i}')
    kb.button(text='🔒 Общий чат', callback_data='general_chat')
    kb.button(text='🔄 Изменить уровень', callback_data='change_level')
    kb.button(text='⬅️ Назад', callback_data='cancel_menu')
    count = 5
    if count <= 4:
        kb.adjust(1)
    elif count <= 10:
        kb.adjust(2)
    else:
        kb.adjust(3)
    return kb.as_markup()
