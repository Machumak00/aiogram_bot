from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

choose_bruteforce_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Instagram")
        ],
        [
            KeyboardButton(text="Отмена")
        ]
    ],
    resize_keyboard=True
)
