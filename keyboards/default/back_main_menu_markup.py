from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

back_main_menu_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="В главное меню")
        ]
    ],
    resize_keyboard=True
)
