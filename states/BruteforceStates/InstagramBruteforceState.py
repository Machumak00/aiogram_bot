from aiogram.dispatcher.filters.state import StatesGroup, State


class InstagramBruteforceState(StatesGroup):
    bruteforce = State()
    username = State()
    mode = State()
    files_count = State()
    password1 = State()
    password2_1 = State()
    password2_2 = State()
