from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

choose_ddos_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="DDos"),
            KeyboardButton(text="DDos через Nmapscan")
        ],
        [
            KeyboardButton(text="В главное меню")
        ]
    ],
    resize_keyboard=True
)
