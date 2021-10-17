from aiogram.dispatcher.filters.state import StatesGroup, State


class IcmpPackDdosHpingState(StatesGroup):
    method = State()
    ip = State()
    port = State()
    stop_script = State()
    stopped_script = State()
