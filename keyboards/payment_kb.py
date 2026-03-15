from aiogram.utils.keyboard import InlineKeyboardBuilder

def subscription_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='✨ Оформить премиум', callback_data='subscribe')
    kb.button(text='⬅️ Назад', callback_data='back_to_profile')
    kb.adjust(1, 1)
    return kb.as_markup()

def payment_method_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='💳 1 способ', callback_data='payment_1')
    kb.button(text='💳 2 способ', callback_data='payment_2')
    kb.button(text='⬅️ Назад в профиль', callback_data='back_to_profile')
    kb.adjust(2, 1)
    return kb.as_markup()