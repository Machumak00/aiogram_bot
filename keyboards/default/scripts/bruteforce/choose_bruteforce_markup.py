from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

choose_bruteforce_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Instagram")
        ],
        [
            KeyboardButton(text="В главное меню")
        ]
    ],
    resize_keyboard=True
)
