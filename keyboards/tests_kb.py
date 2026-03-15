from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.theme_db import get_questions_and_answers

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



