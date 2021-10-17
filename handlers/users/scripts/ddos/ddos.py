from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.default import start_markup
from keyboards.default.scripts.ddos.choose_ddos_markup import choose_ddos_markup
from keyboards.default.scripts.ddos.ddos_hping.choose_ddos_hping_markup import choose_ddos_hping_markup
from keyboards.default.scripts.ddos.scddos_url import choose_scddos_markup
from loader import dp
from states.ddos_states import DdosHpingState
from states.ddos_states import DdosState
from states.ddos_states import ScddosState
from utils.misc import rate_limit


@rate_limit(0.5)
@dp.message_handler(Text(equals=["DDos"]))
async def dos_menu(message: types.Message):
    await message.answer("Вы попали в DDos меню.\n"
                         "Выберите способ DDos-атаки.", reply_markup=choose_ddos_markup)
    await DdosState.ddos.set()


@rate_limit(0.5)
@dp.message_handler(state=DdosState.ddos)
async def enter_dos(message: types.Message, state: FSMContext):
    if message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif message.text in ["Scrypt.DDoS", "High.Ping"]:
        async with state.proxy() as state_data:
            state_data['ddos'] = message.text.lower()
        if message.text == 'Scrypt.DDoS':
            await message.answer("Выберите метод ScDDos-атаки.", reply_markup=choose_scddos_markup)
            await ScddosState.scddos.set()
        elif message.text == 'High.Ping':
            await message.answer("Выберите метод HighPing DDos-атаки.", reply_markup=choose_ddos_hping_markup)
            await DdosHpingState.ddos_hping_options.set()
    else:
        await message.answer("Неверный ввод. Попробуйте ещё раз.")
