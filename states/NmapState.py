from aiogram.dispatcher.filters.state import StatesGroup, State


class NmapState(StatesGroup):
    ip = State()
