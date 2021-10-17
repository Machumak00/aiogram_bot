from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

choose_ddos_hping_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Syn.pack"),
            KeyboardButton(text="Icmp.pack"),
            KeyboardButton(text="Udp.pack"),
            KeyboardButton(text="Pa.pack")
        ],
        [
            KeyboardButton(text="Назад"),
            KeyboardButton(text="В главное меню")
        ]
    ],
    resize_keyboard=True
)
