from aiogram.dispatcher.filters.state import StatesGroup, State


class DosState(StatesGroup):
    dos = State()
    count_script = State()
    ip = State()
    port = State()
    size = State()
    nmap = State()
    stop_script = State()
    stopped_script = State()
