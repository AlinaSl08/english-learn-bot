from aiogram.utils.keyboard import InlineKeyboardBuilder


def profile_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='📊 Статистика', callback_data='statistics')
    kb.button(text='💎 Подписка', callback_data='subscription')
    kb.button(text='⚙️ Настройки', callback_data='settings')
    kb.button(text='⬅️ Назад', callback_data='cancel_menu')
    kb.adjust(2, 2)
    return kb.as_markup()

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

def settings_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='🔄 Изменить уровень', callback_data='change_level')
    kb.button(text='🗑️ Сбросить результаты тестов', callback_data='reset_test_results')
    kb.button(text='⬅️ Назад', callback_data='back_to_profile')
    kb.adjust(1, 1, 1)
    return kb.as_markup()

def reset_confirm_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='✅ Да', callback_data='reset_yes')
    kb.button(text='❌ Нет', callback_data='reset_no')
    kb.adjust(1, 1)
    return kb.as_markup()

def change_level_kb(mode_key=1):
    kb = InlineKeyboardBuilder()
    modes = {1: 'test', 2: 'settings'}
    mode = modes[mode_key]
    if mode == 'test':
        for i in range(1, 5):
            kb.button(text=f'Уровень {i}', callback_data=f'test_level_{i}') #доделать тут
        kb.button(text='⬅️ Назад', callback_data='cancel_menu')
    else: #тут смена уровня в лк
        for i in range(1, 5):
            kb.button(text=f'Уровень {i}', callback_data=f'level_selected_{i}')
        kb.button(text='⬅️ Назад', callback_data='back_to_settings')
    kb.button(text='Сдать тест на уровень', callback_data='test_level')
    count = 5
    if count <= 4:
        kb.adjust(1)
    elif count <= 10:
        kb.adjust(2)
    else:
        kb.adjust(3)
    return kb.as_markup()

