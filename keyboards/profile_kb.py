from aiogram.utils.keyboard import InlineKeyboardBuilder


def profile_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='📊 Статистика', callback_data='statistics')
    kb.button(text='💎 Подписка', callback_data='subscription')
    kb.button(text='⚙️ Настройки', callback_data='settings')
    kb.button(text='⬅️ Назад', callback_data='cancel_menu')
    kb.adjust(2, 2)
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
    levels = ['🍼 Уровень A1', '🐥 Уровень A2', '🎓 Уровень B1', '👨‍🎓 Уровень B2']
    if mode == 'test':
        for idx, level in enumerate(levels, start=1):
            kb.button(text=f'{level}', callback_data=f'test_level_{idx}') #доделать тут
        kb.button(text='⬅️ Назад', callback_data='cancel_menu')
    else: #тут смена уровня в лк
        for idx, level in enumerate(levels, start=1):
            kb.button(text=f'{level}', callback_data=f'level_selected_{idx}')
        kb.button(text='⬅️ Назад', callback_data='back_to_settings')
    kb.button(text='📝 Сдать тест на уровень', callback_data='test_level')
    count = 5
    if count <= 4:
        kb.adjust(1)
    elif count <= 10:
        kb.adjust(2)
    else:
        kb.adjust(3)
    return kb.as_markup()

