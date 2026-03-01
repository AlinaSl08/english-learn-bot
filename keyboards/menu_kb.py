from aiogram.utils.keyboard import InlineKeyboardBuilder

def menu_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='🤵 Профиль', callback_data='profile')
    kb.button(text='📚 Темы', callback_data='theme')
    kb.button(text='📝 Тесты', callback_data='tests')
    kb.button(text='🧠 ИИ-учитель', callback_data='ai_teacher')
    kb.adjust(2, 2)
    return kb.as_markup()