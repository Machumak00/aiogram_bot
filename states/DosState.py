from aiogram.dispatcher.filters.state import StatesGroup, State


class DosState(StatesGroup):
    ip = State()
    port = State()
    size = State()
