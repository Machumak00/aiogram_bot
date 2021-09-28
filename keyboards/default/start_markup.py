from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

start_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="DoS"),
            KeyboardButton(text="Brute Force"),
            KeyboardButton(text="Nmap")
        ],
        [
            KeyboardButton(text="Url Changer"),
            KeyboardButton(text="IP Sniff"),
            KeyboardButton(text="SNAT"),
            KeyboardButton(text="MSFvenom")
        ],
    ],
    resize_keyboard=True
)
