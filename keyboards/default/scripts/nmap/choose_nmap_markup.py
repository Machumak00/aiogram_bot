from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

choose_nmap_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Nmap'),
            KeyboardButton(text='NmapCustom'),
            KeyboardButton(text='Vulners'),
            KeyboardButton(text='VulScan')
        ],
        [
            KeyboardButton(text='В главное меню')
        ]
    ],
    resize_keyboard=True
)
