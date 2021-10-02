from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

choose_mode_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="0"),
            KeyboardButton(text="1"),
            KeyboardButton(text="2"),
            KeyboardButton(text="3")
        ],
        [
            KeyboardButton(text="Назад"),
            KeyboardButton(text="В главное меню")
        ]
    ],
    resize_keyboard=True
)
