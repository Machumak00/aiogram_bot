from aiogram.dispatcher.filters.state import StatesGroup, State


class CrunchState(StatesGroup):
    crunch = State()
    pattern_length = State()
    symbols = State()
    min_length = State()
    max_length = State()
    start_script = State()
