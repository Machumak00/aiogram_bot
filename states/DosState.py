from aiogram.dispatcher.filters.state import StatesGroup, State


class DosState(StatesGroup):
    dos = State()
    ip = State()
    port = State()
    size = State()
    nmap = State()
