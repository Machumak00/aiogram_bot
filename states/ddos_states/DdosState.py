from aiogram.dispatcher.filters.state import StatesGroup, State


class DdosState(StatesGroup):
    ddos = State()
