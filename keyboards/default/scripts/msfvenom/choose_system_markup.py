from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

choose_system_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Windows"),
            KeyboardButton(text="Android")
        ],
        [
            KeyboardButton(text="Отмена")
        ]
    ],
    resize_keyboard=True
)
