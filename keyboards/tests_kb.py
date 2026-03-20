from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.gspread_db import get_questions_and_answers, get_questions_and_answers_level

def questions_kb(theme=1): #сделать замочки если нет премиум
    kb = InlineKeyboardBuilder()
    start_index = (theme - 1) * 5
    for i in range(5):
        current_question_id = start_index + i
        kb.button(text=f'Вопрос {i + 1}', callback_data=f'question_{current_question_id}')
    kb.button(text='⬅️ Назад', callback_data='back_to_theme_test')
    kb.adjust(2, 2, 2)
    return kb.as_markup()


def answers_kb(question_idx):
    kb = InlineKeyboardBuilder()
    start_num = (question_idx - 1) * 3
    for i in range(3):
        current_answer_id = start_num + i
        answer = get_questions_and_answers(current_answer_id)[1]
        kb.button(text=f'{answer}', callback_data=f'answer_{i + 1}')
    kb.button(text='⬅️ Назад', callback_data='back_to_questions_test')
    kb.adjust(2, 2)
    return kb.as_markup()



def start_level_test():
    kb = InlineKeyboardBuilder()
    kb.button(text='🔥 Начать', callback_data='questions_go')
    kb.button(text='⬅️ Вернуться в меню', callback_data='cancel_menu')
    kb.adjust(2, 2)
    return kb.as_markup()



def level_test_answers_kb(question_num=1):
    kb = InlineKeyboardBuilder()
    start_num = (question_num - 1) * 3
    for i in range(3):
        current_answer_id = start_num + i
        answer = get_questions_and_answers_level(current_answer_id)[1]
        kb.button(text=f'{answer}', callback_data=f'testlevel_answer_{i + 1}_question_{question_num + 1}')
    kb.button(text='⬅️ Вернуться в меню', callback_data='cancel_menu')
    kb.adjust(2, 2)
    return kb.as_markup()


def level_test_end():
    kb = InlineKeyboardBuilder()
    kb.button(text=f'🔄 Пройти заново', callback_data=f'test_level')
    kb.button(text='⬅️ Вернуться в меню', callback_data='cancel_menu')
    kb.adjust(2, 2)
    return kb.as_markup()