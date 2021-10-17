from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import start_markup
from keyboards.default.scripts.ddos.choose_ddos_markup import choose_ddos_markup
from keyboards.default.scripts.ddos.ddos_hping import choose_method_markup
from loader import dp
from states.ddos_states import DdosHpingState
from states.ddos_states import DdosState
from states.ddos_states.DdosHpingOptionsState import SynPackDdosHpingState, IcmpPackDdosHpingState, \
    UdpPackDdosHpingState, PaPackDdosHpingState
from utils.misc import rate_limit


@rate_limit(0.5)
@dp.message_handler(state=DdosHpingState.ddos_hping_options)
async def enter_dos(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        async with state.proxy() as state_data:
            state_data.pop("ddos")
        await message.answer("Вы вернулись назад.\nВыберите способ DDos-атаки.", reply_markup=choose_ddos_markup)
        await DdosState.ddos.set()
    elif message.text == "В главное меню":
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif message.text in ["Syn.pack", "Icmp.pack", "Udp.pack", "Pa.pack"]:
        async with state.proxy() as state_data:
            state_data["ddos_hping_options"] = message.text.lower()
        await message.answer("Выберите вариацию атаки. Стандартный вариант рекомендуется для неопытных пользователей.",
                             reply_markup=choose_method_markup)
        if message.text == "Syn.pack":
            await message.answer("Стандартные параметры для SynPack:\n"
                                 "• количество пакетов - 15000;\n"
                                 "• количество байтов - 500;\n"
                                 "• порт - 80.\n")
            await SynPackDdosHpingState.method.set()
        elif message.text == "Icmp.pack":
            await message.answer("Стандартные параметры для IcmpPack:\n"
                                 "• количество байтов - 500;\n")
            await IcmpPackDdosHpingState.method.set()
        elif message.text == "Udp.pack":
            await message.answer("Стандартные параметры для UdpPack:\n"
                                 "• порт - 443.\n")
            await UdpPackDdosHpingState.method.set()
        elif message.text == "Pa.pack":
            await message.answer("Стандартные параметры для PaPack:\n"
                                 "• количество пакетов - 200000;\n"
                                 "• количество байтов - 400;\n"
                                 "• порт - 443.\n")
            await PaPackDdosHpingState.method.set()
    else:
        await message.answer("Неверный ввод. Попробуйте ещё раз.")
