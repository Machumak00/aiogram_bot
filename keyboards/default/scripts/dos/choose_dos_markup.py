from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

choose_dos_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="DoS"),
            KeyboardButton(text="DoS через Nmap")
        ],
        [
            KeyboardButton(text="В главное меню")
        ]
    ],
    resize_keyboard=True
)
