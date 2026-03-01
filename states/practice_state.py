from aiogram.fsm.state import StatesGroup, State

class Practice(StatesGroup):
    level = State()
    theme = State()
    question = State()
    answer = State()