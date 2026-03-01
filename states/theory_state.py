from aiogram.fsm.state import StatesGroup, State

class Theory(StatesGroup):
    level = State()
    theme = State()
    subtopic = State()