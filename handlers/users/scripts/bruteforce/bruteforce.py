import asyncio
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import data
from keyboards.default import start_markup, back_menu_markup
from keyboards.default.scripts.bruteforce import choose_bruteforce_markup, choose_files_count_markup, choose_mode_markup
from loader import dp
from states import InstagramBruteforceState
from utils.misc import rate_limit, script_wait_message
from utils.scripts.bruteforce.instagram import start_bruteforce_instagram


@rate_limit(0.5)
@dp.message_handler(Text(equals=["BruteForce"]))
async def bruteforce_menu(message: types.Message):
    await message.answer("Вы попали в BruteForce меню.\n"
                         "Выберите, что хотите взломать.", reply_markup=choose_bruteforce_markup)
    await InstagramBruteforceState.bruteforce.set()


@rate_limit(0.5)
@dp.message_handler(state=InstagramBruteforceState.bruteforce)
async def enter_bruteforce(message: types.Message, state: FSMContext):
    if message.text == 'Instagram':
        async with state.proxy() as state_data:
            state_data['bruteforce'] = message.text
        await message.answer("Введите логин пользователя.", reply_markup=back_menu_markup)
        await InstagramBruteforceState.username.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод метода. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
        return
    else:
        await message.answer("Нет такого метода. Попробуйте ещё раз.")
        await InstagramBruteforceState.bruteforce.set()
        return


@rate_limit(0.5)
@dp.message_handler(state=InstagramBruteforceState.username)
async def enter_username(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('bruteforce')
        await message.answer("Вы вернулись в BruteForce меню.\n"
                             "Выберите, что хотите взломать.", reply_markup=choose_bruteforce_markup)
        await InstagramBruteforceState.bruteforce.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод логина пользователя. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    else:
        async with state.proxy() as state_data:
            state_data['username'] = message.text
        await message.answer("Выберите параметр мод.", reply_markup=choose_mode_markup)
        await InstagramBruteforceState.mode.set()


@rate_limit(0.5)
@dp.message_handler(state=InstagramBruteforceState.mode)
async def enter_mode(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('username')
        await message.answer("Вы вернулись в меню ввода логина пользователя.\n"
                             "Введите логин пользователя.", reply_markup=back_menu_markup)
        await InstagramBruteforceState.username.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили выбор мода. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif message.text in ['0', '1', '2', '3']:
        async with state.proxy() as state_data:
            state_data['mode'] = message.text
        await message.answer("Выберите количество файлов с паролями.", reply_markup=choose_files_count_markup)
        await InstagramBruteforceState.files_count.set()
    else:
        await message.answer("Неверный ввод мода. Попробуйте ещё раз.")
        await InstagramBruteforceState.mode.set()


@rate_limit(0.5)
@dp.message_handler(state=InstagramBruteforceState.files_count)
async def enter_files_count(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('mode')
        await message.answer("Вы вернулись в меню ввода мода.\n"
                             "Введите мод.", reply_markup=choose_mode_markup)
        await InstagramBruteforceState.mode.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили выбор количества файлов. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif message.text == '1':
        async with state.proxy() as state_data:
            state_data['files_count'] = message.text
        await message.answer("Загрузите файл.", reply_markup=back_menu_markup)
        await InstagramBruteforceState.password1.set()
    elif message.text == '2':
        async with state.proxy() as state_data:
            state_data['files_count'] = message.text
        await message.answer("Вы выбрали загрузку 2-ух файлов. Пожалуйста, загрузите первый.",
                             reply_markup=back_menu_markup)
        await InstagramBruteforceState.password2_1.set()
    else:
        await message.answer("Неверный ввод количества файлов. Попробуйте ещё раз.")
        await InstagramBruteforceState.files_count.set()


@rate_limit(0.5)
@dp.message_handler(state=InstagramBruteforceState.password1, content_types=['text', 'document'])
async def enter_password1(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('files_count')
        await message.answer("Вы вернулись в меню выбора количества файлов.\n"
                             "Выберите количество файлов с паролями.", reply_markup=choose_files_count_markup)
        await InstagramBruteforceState.files_count.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили загрузку файла. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
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


@rate_limit(0.5)
@dp.message_handler(state=InstagramBruteforceState.password2_1, content_types=['text', 'document'])
async def enter_password2_1(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('files_count')
        await message.answer("Вы вернулись в меню выбора количества файлов.\n"
                             "Выберите количество файлов с паролями.", reply_markup=choose_files_count_markup)
        await InstagramBruteforceState.files_count.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили загрузку файла. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif message.document:
        user_path = os.path.dirname(os.path.abspath(data.users.__file__)) + \
                    f"/user_{message.from_user.id}/scripts/bruteforce/instagram/passwords/"
        current_file = 'file1'
        async with state.proxy() as state_data:
            state_data[current_file] = user_path
            await message.document.download(destination_file=user_path + 'file1.txt')
        await message.answer("Загрузите второй файл.", reply_markup=back_menu_markup)
        await InstagramBruteforceState.password2_2.set()
    else:
        await message.answer("Неверный ввод файла. Попробуйте ещё раз")
        await InstagramBruteforceState.password2_1.set()


@rate_limit(0.5)
@dp.message_handler(state=InstagramBruteforceState.password2_2, content_types=['text', 'document'])
async def enter_password2_2(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('file1')
        await message.answer("Вы вернулись в меню загрузки первого файла.\n"
                             "Пожалуйста, загрузите файл.")
        await InstagramBruteforceState.password2_1.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили загрузку файла. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif message.document:
        user_id = message.from_user.id
        user_path = os.path.dirname(os.path.abspath(data.users.__file__)) + \
                    f"/user_{user_id}/scripts/bruteforce/instagram/passwords/"
        current_file = 'file2'
        async with state.proxy() as state_data:
            state_data[current_file] = user_path
            await message.document.download(destination_file=user_path + 'file2.txt')
            await message.answer('Скрипт выполняется...')
            await InstagramBruteforceState.start_script.set()
            tasks = [
                start_bruteforce_instagram(state_data),
                script_wait_message(message)
            ]
            finished, unfinished = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in unfinished:
                task.cancel()
            await state.reset_state()
            await message.answer("Скрипт успешно выполнен.\n"
                                 "Возврат в главное меню. Выберите эксплойт.", reply_markup=start_markup)
    else:
        await message.answer("Неверный ввод файла. Попробуйте ещё раз")
        await InstagramBruteforceState.password2_2.set()


@dp.message_handler(state=InstagramBruteforceState.start_script)
async def enter_password2_1(message: types.Message, state: FSMContext):
    await message.answer("Подождите, скрипт ещё выполняется.")
