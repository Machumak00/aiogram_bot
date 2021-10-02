from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

back_menu_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Назад"),
            KeyboardButton(text="В главное меню")
        ]
    ],
    resize_keyboard=True
)
