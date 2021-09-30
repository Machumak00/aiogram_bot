import logging
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
from utils.misc.files import create_dirs
from utils.scripts.bruteforce.instagram import start_bruteforce_instagram


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
        await message.answer("Нет такого метода. Попробуйте ещё раз.")
        await InstagramBruteforceState.bruteforce.set()
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
        await message.answer("Неверный ввод мода. Попробуйте ещё раз.")
        await InstagramBruteforceState.mode.set()
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
        await message.answer("Неверный ввод количества файлов. Попробуйте ещё раз.")
        await InstagramBruteforceState.files_count.set()
        return


@dp.message_handler(state=InstagramBruteforceState.password1, content_types=['text', 'document'])
async def enter_password1(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.reset_state()
        await message.answer("Вы отменили загрузку файла. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return
    elif message.document:
        user_id = message.from_user.id
        user_path = os.path.dirname(os.path.abspath(data.users.__file__)) + \
                    f"/user_{user_id}/scripts/bruteforce/instagram/passwords/"
        current_file = 'file1'
        async with state.proxy() as state_data:
            state_data[current_file] = user_path
            await message.document.download(destination_file=user_path + 'file1.txt')
            await message.answer('Скрипт выполняется...')
            await start_bruteforce_instagram(state_data)
        await message.answer("Скрипт успешно выполнен.\n"
                             "Возврат в главное меню. Выберите эксплойт.", reply_markup=start_markup)
        await state.reset_state()
    else:
        await message.answer("Неверный ввод файла. Попробуйте ещё раз")
        await InstagramBruteforceState.password1.set()
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
                    f"/user_{message.from_user.id}/scripts/bruteforce/instagram/passwords/"
        current_file = 'file1'
        async with state.proxy() as state_data:
            state_data[current_file] = user_path
            await message.document.download(destination_file=user_path + 'file1.txt')
        await message.answer("Загрузите второй файл.", reply_markup=cancel_markup)
        await InstagramBruteforceState.password2_2.set()
    else:
        await message.answer("Неверный ввод файла. Попробуйте ещё раз")
        await InstagramBruteforceState.password2_1.set()
        return


@dp.message_handler(state=InstagramBruteforceState.password2_2, content_types=['text', 'document'])
async def enter_password2_2(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.reset_state()
        await message.answer("Вы отменили загрузку файла. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return
    elif message.document:
        user_id = message.from_user.id
        user_path = os.path.dirname(os.path.abspath(data.users.__file__)) + \
                    f"/user_{user_id}/scripts/bruteforce/instagram/passwords/"
        current_file = 'file2'
        async with state.proxy() as state_data:
            state_data[current_file] = user_path
            await message.document.download(destination_file=user_path + 'file2.txt')
            await message.answer('Скрипт выполняется...')
            await start_bruteforce_instagram(state_data)
        await message.answer("Скрипт успешно выполнен.\n"
                             "Возврат в главное меню. Выберите эксплойт.", reply_markup=start_markup)
        await state.reset_state()
    else:
        await message.answer("Неверный ввод файла. Попробуйте ещё раз")
        await InstagramBruteforceState.password2_2.set()
        return
