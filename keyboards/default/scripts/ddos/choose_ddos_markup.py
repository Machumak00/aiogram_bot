from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

choose_ddos_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Scrypt.DDoS"),
            KeyboardButton(text="High.Ping")
        ],
        [
            KeyboardButton(text="В главное меню")
        ]
    ],
    resize_keyboard=True
)
