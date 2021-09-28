import os
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import data
from keyboards.default import start_markup, cancel_markup
from keyboards.default.scripts.bruteforce import choose_bruteforce_markup, choose_files_count_markup, choose_mode_markup
from loader import dp
from states import InstagramBruteforceState
from utils.misc import rate_limit


@rate_limit(5, key='BruteForce')
@dp.message_handler(Text(equals=["BruteForce"]))
async def bruteforce_menu(message: types.Message):
    await message.answer("Вы попали в BruteForce меню.\n"
                         "Выберите, что хотите взломать.", reply_markup=choose_bruteforce_markup)
    await InstagramBruteforceState.bruteforce.set()


@dp.message_handler(state=InstagramBruteforceState.bruteforce)
async def enter_bruteforce(message: types.Message, state: FSMContext):
    if message.text == 'Instagram':
        async with state.proxy() as data:
            data['bruteforce'] = message.text
        await message.answer("Введите username пользователя.", reply_markup=cancel_markup)
        await InstagramBruteforceState.username.set()
    elif message.text == 'Отмена':
        await state.reset_state()
        await message.answer("Вы отменили ввод метода. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return
    else:
        await state.reset_state()
        await message.answer("Нет такого метода. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return


@dp.message_handler(state=InstagramBruteforceState.username)
async def enter_username(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.reset_state()
        await message.answer("Вы отменили ввод логина пользователя. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return
    async with state.proxy() as data:
        data['username'] = message.text
    await message.answer("Выберите параметр мод.", reply_markup=choose_mode_markup)
    await InstagramBruteforceState.mode.set()


@dp.message_handler(state=InstagramBruteforceState.mode)
async def enter_mode(message: types.Message, state: FSMContext):
    if message.text in ['0', '1', '2', '3']:
        async with state.proxy() as data:
            data['mode'] = message.text
        await message.answer("Выберите количество файлов с паролями.", reply_markup=choose_files_count_markup)
        await InstagramBruteforceState.files_count.set()
    elif message.text == 'Отмена':
        await state.reset_state()
        await message.answer("Вы отменили выбор мода. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return
    else:
        await state.reset_state()
        await message.answer("Неверный ввод количества файлов. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return


@dp.message_handler(state=InstagramBruteforceState.files_count)
async def enter_files_count(message: types.Message, state: FSMContext):
    if message.text == '1':
        async with state.proxy() as data:
            data['files_count'] = message.text
        await message.answer("Загрузите файл.", reply_markup=cancel_markup)
        await InstagramBruteforceState.password1.set()
    elif message.text == '2':
        async with state.proxy() as data:
            data['files_count'] = message.text
        await message.answer("Вы выбрали загрузку 2-ух файлов. Пожалуйста, загрузите первый.",
                             reply_markup=cancel_markup)
        await InstagramBruteforceState.password2_1.set()
    elif message.text == 'Отмена':
        await state.reset_state()
        await message.answer("Вы отменили выбор количества файлов. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return
    else:
        await state.reset_state()
        await message.answer("Неверный ввод количества файлов. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return


@dp.message_handler(state=InstagramBruteforceState.password1, content_types=['text', 'document'])
async def enter_password1(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.reset_state()
        await message.answer("Вы отменили загрузку файла. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return
    elif message.document:
        user_path = os.path.dirname(os.path.abspath(data.users.__file__)) + \
                    f"/user_{message.from_user.id}/scripts/bruteforce/instagram/passwords"
        if not os.path.exists(user_path):
            os.makedirs(user_path)
        async with state.proxy() as state_data:
            state_data['file1'] = user_path
        await message.document.download(destination_dir=user_path)
        await message.answer('Скрипт выполняется...')
        await sleep(3)  # script here
        await message.answer("Скрипт успешно выполнен.\n"
                             "Возврат в главное меню. Выберите эксплойт.", reply_markup=start_markup)
        await state.reset_state()
    else:
        await state.reset_state()
        await message.answer("Неверный ввод файла. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return


@dp.message_handler(state=InstagramBruteforceState.password2_1, content_types=['text', 'document'])
async def enter_password2_1(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.reset_state()
        await message.answer("Вы отменили загрузку файла. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return
    elif message.document:
        user_path = os.path.dirname(os.path.abspath(data.users.__file__)) + \
                    f"/user_{message.from_user.id}/scripts/bruteforce/instagram/passwords"
        if not os.path.exists(user_path):
            os.makedirs(user_path)
        async with state.proxy() as state_data:
            state_data['file1'] = user_path
        await message.document.download(destination_dir=user_path)
        await message.answer("Загрузите второй файл.", reply_markup=cancel_markup)
        await InstagramBruteforceState.password2_2.set()
    else:
        await state.reset_state()
        await message.answer("Неверный ввод файла. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return


@dp.message_handler(state=InstagramBruteforceState.password2_2, content_types=['text', 'document'])
async def enter_password2_2(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.reset_state()
        await message.answer("Вы отменили загрузку файла. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return
    elif message.document:
        user_path = os.path.dirname(os.path.abspath(data.users.__file__)) + \
                    f"/user_{message.from_user.id}/scripts/bruteforce/instagram/passwords"
        if not os.path.exists(user_path):
            os.makedirs(user_path)
        async with state.proxy() as state_data:
            state_data['file2'] = user_path
        await message.document.download(destination_dir=user_path)
        await message.answer('Скрипт выполняется...')
        await sleep(3)  # script here
        await message.answer("Скрипт успешно выполнен.\n"
                             "Возврат в главное меню. Выберите эксплойт.", reply_markup=start_markup)
        await state.reset_state()
    else:
        await state.reset_state()
        await message.answer("Неверный ввод файла. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return
