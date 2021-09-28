from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

cancel_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Отмена")
        ]
    ],
    resize_keyboard=True
)
