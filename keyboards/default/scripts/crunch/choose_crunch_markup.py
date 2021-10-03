from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

choose_crunch_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="С шаблоном"),
            KeyboardButton(text="Без шаблона"),
            KeyboardButton(text="RckU")
        ],
        [
            KeyboardButton(text="В главное меню")
        ]
    ],
    resize_keyboard=True
)
