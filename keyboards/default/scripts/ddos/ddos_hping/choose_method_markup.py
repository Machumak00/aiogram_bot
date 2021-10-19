from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

choose_method_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Standard"),
            KeyboardButton(text="Custom")
        ],
        [
            KeyboardButton(text="Назад"),
            KeyboardButton(text="В главное меню")
        ]
    ],
    resize_keyboard=True
)
