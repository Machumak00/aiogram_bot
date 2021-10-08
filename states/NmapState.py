from aiogram.dispatcher.filters.state import StatesGroup, State


class NmapState(StatesGroup):
    nmap = State()
    custom_args = State()
    ip = State()
    start_script = State()
