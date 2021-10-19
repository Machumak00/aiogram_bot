import asyncio
import os
from os.path import sep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import data
import utils
from keyboards.default import start_markup, back_menu_markup
from keyboards.default.scripts.passgen import choose_passgen_markup
from loader import dp
from states.PassgenState import PassgenState
from utils.misc import rate_limit, script_wait_message
from utils.misc.files import delete_directory_files
from utils.scripts.passgen import start_passgen
from utils.scripts.passgen.start_passgen import do_key_interrupt


@rate_limit(0.5)
@dp.message_handler(Text(equals=["PassGen"]))
async def crunch_menu(message: types.Message):
    await message.answer("Вы попали в Crunch меню.\n"
                         "Введите способ генерации пароля.", reply_markup=choose_passgen_markup)
    await PassgenState.passgen.set()


@rate_limit(0.5)
@dp.message_handler(state=PassgenState.passgen)
async def enter_bruteforce(message: types.Message, state: FSMContext):
    if message.text == 'С шаблоном':
        async with state.proxy() as state_data:
            state_data['is_template'] = True
        await message.answer("Введите длину пароля: от 1 до 12 символов.",
                             reply_markup=back_menu_markup)
        await PassgenState.pattern_length.set()
    elif message.text == 'Без шаблона':
        async with state.proxy() as state_data:
            state_data['is_template'] = False
        await message.answer("Введите минимальную длину пароля: от 1 до 12 символов.",
                             reply_markup=back_menu_markup)
        await PassgenState.min_length.set()
    elif message.text == 'RckU':
        await message.answer("Идёт загрузка файлов. Пожалуйста, подождите...")
        await PassgenState.download_files.set()
        pass_path = os.path.dirname(
            os.path.abspath(utils.scripts.passgen.__file__)) + os.path.sep + 'rcku' + os.path.sep
        files = [open(pass_path + '%d.txt' % i, 'r') for i in range(3)]
        for file in files:
            await message.answer_document(file)
            file.close()
        await message.answer("Все файлы были загружены.")
        await PassgenState.passgen.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    else:
        await message.answer("Неверный ввод. Попробуйте ещё раз.")


@dp.message_handler(state=PassgenState.download_files)
async def enter_password2_1(message: types.Message, state: FSMContext):
    await message.answer("Подождите, файлы ещё загружаются.")


@rate_limit(0.5)
@dp.message_handler(state=PassgenState.pattern_length)
async def enter_username(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('passgen')
        await message.answer("Вы вернулись в Crunch меню.\n"
                             "Введите способ генерации пароля.", reply_markup=choose_passgen_markup)
        await PassgenState.passgen.set()
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
            await PassgenState.symbols.set()
        else:
            await message.answer("Вы ввели число не из диапазона [1; 12]. Попробуйте ещё раз.")
    else:
        await message.answer("Вы ввели не число. Попробуйте ещё раз.")


@rate_limit(0.5)
@dp.message_handler(state=PassgenState.symbols)
async def enter_username(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('passgen')
        await message.answer("Вы вернулись назад.\nВведите длину пароля: от 1 до 12 символов.")
        await PassgenState.pattern_length.set()
    elif message.text == 'В главное меню':
        await state.reset_state()
        await message.answer("Вы отменили ввод данных. Возврат в главное меню.\n"
                             "Выберите эксплойт.", reply_markup=start_markup)
    elif len(message.text) == (await state.get_data())['min_length']:
        async with state.proxy() as state_data:
            state_data['symbols'] = message.text
            await message.answer('Скрипт выполняется...')
            await PassgenState.start_script.set()
            users_data_path = os.path.dirname(os.path.abspath(data.users.__file__)) + \
                              f"{sep}user_{message.from_user.id}{sep}scripts{sep}passgen"
            tasks = [
                do_key_interrupt(),
                start_passgen(users_data_path, state_data),
                script_wait_message(message)
            ]
            finished, unfinished = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in unfinished:
                task.cancel()
            for task in finished:
                if task.result() == True:
                    await state.reset_state()
                    await message.answer("Скрипт был прерван, слишком большой таймаут.\n"
                                         "Возврат в главное меню. Выберите эксплойт.",
                                         reply_markup=start_markup)
                    delete_directory_files(users_data_path)
                    return
            with open(users_data_path + os.path.sep + "passwords.txt") as f:
                await message.answer_document(f)
            delete_directory_files(users_data_path)
            await state.reset_state()
            await message.answer("Скрипт успешно выполнен.\n"
                                 "Возврат в главное меню. Выберите эксплойт.", reply_markup=start_markup)
    else:
        await message.answer("Неверная длина пароля. Попробуйте ещё раз.")


@rate_limit(0.5)
@dp.message_handler(state=PassgenState.min_length)
async def enter_username(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('passgen')
        await message.answer("Вы вернулись в Crunch меню.\n"
                             "Введите способ генерации пароля.", reply_markup=choose_passgen_markup)
        await PassgenState.passgen.set()
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
            await PassgenState.max_length.set()
        else:
            await message.answer("Вы ввели число не из диапазона [1; 12]. Попробуйте ещё раз.")
    else:
        await message.answer("Вы ввели не число. Попробуйте ещё раз.")


@rate_limit(0.5)
@dp.message_handler(state=PassgenState.max_length)
async def enter_mode(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        async with state.proxy() as state_data:
            state_data.pop('min_length')
        await message.answer("Вы вернулись.\n"
                             "Введите минимальную длину пароля.", reply_markup=choose_passgen_markup)
        await PassgenState.passgen.set()
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
                    await PassgenState.start_script.set()
                    users_data_path = os.path.dirname(os.path.abspath(data.users.__file__)) + \
                                      f"{sep}user_{message.from_user.id}{sep}scripts{sep}passgen"
                    tasks = [
                        do_key_interrupt(),
                        start_passgen(users_data_path, state_data),
                        script_wait_message(message)
                    ]
                    finished, unfinished = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                    for task in unfinished:
                        task.cancel()
                    for task in finished:
                        if task.result() == True:
                            await state.reset_state()
                            await message.answer("Скрипт был прерван, слишком большой таймаут.\n"
                                                 "Возврат в главное меню. Выберите эксплойт.",
                                                 reply_markup=start_markup)
                            delete_directory_files(users_data_path)
                            return
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


@dp.message_handler(state=PassgenState.start_script)
async def start_script(message: types.Message, state: FSMContext):
    await message.answer("Подождите, скрипт ещё выполняется.")
