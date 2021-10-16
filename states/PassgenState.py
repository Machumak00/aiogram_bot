from aiogram.dispatcher.filters.state import StatesGroup, State


class PassgenState(StatesGroup):
    passgen = State()
    download_files = State()
    pattern_length = State()
    symbols = State()
    min_length = State()
    max_length = State()
    start_script = State()
