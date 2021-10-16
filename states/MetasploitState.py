from aiogram.dispatcher.filters.state import StatesGroup, State


class MetasploitState(StatesGroup):
    system = State()
    ip = State()
    port = State()
    file_name = State()
