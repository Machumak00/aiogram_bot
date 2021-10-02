from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

choose_files_count_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="1"),
            KeyboardButton(text="2")
        ],
        [
            KeyboardButton(text="Назад"),
            KeyboardButton(text="В главное меню")
        ]
    ],
    resize_keyboard=True
)
