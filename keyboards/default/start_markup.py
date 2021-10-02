from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

start_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="MSFvenom"),
            KeyboardButton(text="BruteForce"),
            KeyboardButton(text="UrlChanger")
        ],
        [
            KeyboardButton(text="Nmap"),
            KeyboardButton(text="DoS"),
            KeyboardButton(text="SNAT"),
            KeyboardButton(text="IpSniff")
        ],
    ],
    resize_keyboard=True
)
