import asyncio
import logging
import os
from asyncio import sleep

import aiogram.types
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import utils
from keyboards.default import start_markup, back_menu_markup
from keyboards.default.scripts.crunch import choose_crunch_markup
from loader import dp
from states.CrunchState import CrunchState
from utils.misc import rate_limit, script_wait_message
from utils.misc.files import delete_directory_files
from utils.scripts.crunch import start_crunch


@rate_limit(0.5)
@dp.message_handler(Text(equals=["Crunch"]))
async def crunch_menu(message: types.Message):
    await message.answer("Вы попали в Crunch меню.\n"
                         "Введите способ генерации пароля.", reply_markup=choose_crunch_markup)
    await CrunchState.crunch.set()


@rate_limit(0.5)
@dp.message_handler(state=CrunchState.crunch)
async def enter_bruteforce(message: types.Message, state: FSMContext):
    if message.text == 'С шаблоном':
        async with state.proxy() as state_data:
            state_data['is_template'] = True
        await message.answer("Введите длину пароля: от 1 до 12 символов.",
                             reply_markup=back_menu_markup)
        await CrunchState.pattern_length.set()
    elif message.text == 'Без шаблона':
        async with state.proxy() as state_data:
            state_data['is_template'] = False
        await message.answer("Введите минимальную длину пароля: от 1 до 12 символов.",
                             reply_markup=back_menu_markup)
        await CrunchState.min_length.set()
    elif message.text == 'RckU':
        await message.answer("Идёт загрузка файла. Пожалуйста, подождите...")
        # Создать 3 файла, чтобы можно было загружать их пользователю. Эту хуету я оставлю пока что.
        # Да и вообще надо куда-то сохранить, потому что можно будет большие файлы в дальнейшем на лету скидывать
        #   пользователю
        # number_of_files = 3
        # users_path = os.path.dirname(os.path.abspath(utils.scripts.crunch.__file__)) + os.path.sep
        # with open(users_path + 'rockyou.txt', 'r', encoding='utf-8', errors='ignore') as infp:
        #     files = [open(users_path + '%d.txt' % i, 'w', encoding='utf-8', errors='ignore') for i in range(number_of_files)]
        #     for i, line in enumerate(infp):
        #         files[i % number_of_files].write(line)
        #     for f in files:
        #         f.close()
        await message.answer("Все файлы были загружены.")
        await CrunchState.crunch.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    else:
        await message.answer("Неверный ввод. Попробуйте ещё раз.")


@rate_limit(0.5)
@dp.message_handler(state=CrunchState.pattern_length)
async def enter_username(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('crunch')
        await message.answer("Вы вернулись в Crunch меню.\n"
                             "Введите способ генерации пароля.", reply_markup=choose_crunch_markup)
        await CrunchState.crunch.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif message.text.isnumeric():
        length = int(message.text)
        if length in range(1, 13):
            async with state.proxy() as state_data:
                state_data['min_length'] = length
                state_data['max_length'] = length
            await message.answer("Введите шаблон. Отметьте знаком '@' те символы, которые вы не знаете.\n"
                                 "Пример: если Вы ввели длину пароля 6 и знаете, что цифры 1, 2 и 3 "
                                 "находятся на первом, третьем и шестом местах соответственно, то Ваш "
                                 "ввод будет выглядеть следующим образом: 1@2@@3",
                                 reply_markup=back_menu_markup)
            await CrunchState.symbols.set()
        else:
            await message.answer("Вы ввели число не из диапазона [1; 12]. Попробуйте ещё раз.")
    else:
        await message.answer("Вы ввели не число. Попробуйте ещё раз.")


@rate_limit(0.5)
@dp.message_handler(state=CrunchState.symbols)
async def enter_username(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('crunch')
        await message.answer("Вы вернулись назад.\nВведите длину пароля: от 1 до 12 символов.")
        await CrunchState.pattern_length.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif len(message.text) == (await state.get_data())['min_length']:
        async with state.proxy() as state_data:
            state_data['symbols'] = message.text
            await message.answer('Скрипт выполняется...')
            await CrunchState.start_script.set()
            tasks = [
                script_wait_message(message),
                start_crunch(message.from_user.id, state_data)
            ]
            finished, unfinished = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in unfinished:
                task.cancel()
            users_data_path = ''
            for task in finished:
                users_data_path = task.result()
            with open(users_data_path + os.path.sep + "passwords.txt") as f:
                await message.answer_document(f)
            delete_directory_files(users_data_path)
            await state.reset_state()
            await message.answer("Скрипт успешно выполнен.\n"
                                 "Возврат в главное меню. Выберите эксплойт.", reply_markup=start_markup)
    else:
        await message.answer("Неверная длина пароля. Попробуйте ещё раз.")


@rate_limit(0.5)
@dp.message_handler(state=CrunchState.min_length)
async def enter_username(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('crunch')
        await message.answer("Вы вернулись в Crunch меню.\n"
                             "Введите способ генерации пароля.", reply_markup=choose_crunch_markup)
        await CrunchState.crunch.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif message.text.isnumeric():
        min_length = int(message.text)
        if min_length in range(1, 13):
            async with state.proxy() as state_data:
                state_data['min_length'] = min_length
            await message.answer("Введите максимальную длину пароля: от 1 до 12 символов.\n"
                                 "Максимальная длина пароля должна быть больше или равна минимальной длины.",
                                 reply_markup=back_menu_markup)
            await CrunchState.max_length.set()
        else:
            await message.answer("Вы ввели число не из диапазона [1; 12]. Попробуйте ещё раз.")
    else:
        await message.answer("Вы ввели не число. Попробуйте ещё раз.")


@rate_limit(0.5)
@dp.message_handler(state=CrunchState.max_length)
async def enter_mode(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('min_length')
        await message.answer("Вы вернулись.\n"
                             "Введите минимальную длину пароля.", reply_markup=choose_crunch_markup)
        await CrunchState.crunch.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif message.text.isnumeric():
        max_length = int(message.text)
        if max_length in range(1, 13):
            min_length = (await state.get_data())['min_length']
            if max_length >= min_length:
                async with state.proxy() as state_data:
                    state_data['max_length'] = message.text
                    await message.answer('Скрипт выполняется...')
                    await CrunchState.start_script.set()
                    tasks = [
                        script_wait_message(message),
                        start_crunch(message.from_user.id, state_data)
                    ]
                    finished, unfinished = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                    for task in unfinished:
                        task.cancel()
                    users_data_path = ''
                    for task in finished:
                        users_data_path = task.result()
                    with open(users_data_path + os.path.sep + "passwords.txt") as f:
                        await message.answer_document(f)
                    delete_directory_files(users_data_path)
                    await state.reset_state()
                    await message.answer("Скрипт успешно выполнен.\n"
                                         "Возврат в главное меню. Выберите эксплойт.", reply_markup=start_markup)
            else:
                await message.answer("Максимальная длина пароля не может быть меньше минимальной. Попробуйте ещё раз.")
        else:
            await message.answer("Вы ввели число не из диапазона [1; 12]. Попробуйте ещё раз.")
    else:
        await message.answer("Вы ввели не число. Попробуйте ещё раз.")


@dp.message_handler(state=CrunchState.start_script)
async def enter_password2_1(message: types.Message, state: FSMContext):
    await message.answer("Подождите, скрипт ещё выполняется.")
