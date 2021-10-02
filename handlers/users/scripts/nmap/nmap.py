from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.default import start_markup, back_menu_markup
from loader import dp
from states import NmapState
from utils.misc import rate_limit
from utils.scripts.nmap.start_nmap import start_nmap


@rate_limit(5, key='Nmap')
@dp.message_handler(Text(equals=["Nmap"]))
async def nmap_menu(message: types.Message):
    await message.answer("Вы попали в Nmap меню.\n"
                         "Введите IP-адрес.", reply_markup=back_menu_markup)
    await NmapState.ip.set()


@dp.message_handler(state=NmapState.ip)
async def enter_ip(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.reset_state()
        await message.answer("Вы отменили ввод IP-адреса. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return
    async with state.proxy() as data:
        data['ip'] = message.text
    await message.answer('Скрипт выполняется...')
    stdout = await start_nmap(data)
    await message.answer(stdout.decode('utf-8'), disable_web_page_preview=True)
    await message.answer("Скрипт успешно выполнен.\n"
                         "Возврат в главное меню. Выберите эксплойт.", reply_markup=start_markup)
    await state.reset_state()
