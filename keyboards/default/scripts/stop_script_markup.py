from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

stop_script_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="STOP"),
        ]
    ],
    resize_keyboard=True
)
