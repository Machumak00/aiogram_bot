from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

start_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="MSFvenom"),
            KeyboardButton(text="Brute Force"),
            KeyboardButton(text="Url Changer")
        ],
        [
            KeyboardButton(text="Nmap"),
            KeyboardButton(text="DoS"),
            KeyboardButton(text="SNAT"),
            KeyboardButton(text="IP Sniff")
        ],
    ],
    resize_keyboard=True
)
