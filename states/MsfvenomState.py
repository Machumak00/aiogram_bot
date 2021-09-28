from aiogram.dispatcher.filters.state import StatesGroup, State


class MsfvenomState(StatesGroup):
    system = State()
    ip = State()
    port = State()
    file_name = State()
