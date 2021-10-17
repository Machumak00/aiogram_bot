from aiogram.dispatcher.filters.state import StatesGroup, State


class SynPackDdosHpingState(StatesGroup):
    method = State()
    ip = State()
    port = State()
    bytes_count = State()
    packages_count = State()
    stop_script = State()
    stopped_script = State()
