from aiogram.dispatcher.filters.state import StatesGroup, State


class DdosHpingState(StatesGroup):
    ddos_hping_options = State()
