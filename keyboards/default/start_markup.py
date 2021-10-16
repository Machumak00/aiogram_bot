from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

start_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Metasploit"),
            KeyboardButton(text="Bruteforce"),
            # KeyboardButton(text="UrlChanger")
        ],
        [
            KeyboardButton(text="NmapScan"),
            KeyboardButton(text="DDos"),
            KeyboardButton(text="PassGen"),
            # KeyboardButton(text="SNAT"),
            # KeyboardButton(text="IpSniff")
        ]
    ],
    resize_keyboard=True
)
