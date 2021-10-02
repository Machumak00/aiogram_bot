from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

start_script_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Запуск")
        ],
        [
            KeyboardButton(text="Назад"),
            KeyboardButton(text="В главное меню")
        ]
    ],
    resize_keyboard=True
)
