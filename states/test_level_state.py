from aiogram.fsm.state import StatesGroup, State

class TestLevel(StatesGroup):
    question0 = State()
    question1 = State()
    question2 = State()
    question3 = State()
    question4 = State()
    question5 = State()
    question6 = State()
    question7 = State()
    question8 = State()
    question9 = State()
    question10 = State()
    question_completed = State()