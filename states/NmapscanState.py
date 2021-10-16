from aiogram.dispatcher.filters.state import StatesGroup, State


class NmapscanState(StatesGroup):
    nmapscan = State()
    custom_args = State()
    ip = State()
    start_script = State()
