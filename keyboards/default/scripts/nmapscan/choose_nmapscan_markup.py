from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

choose_nmapscan_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Nmapscan'),
            KeyboardButton(text='NmapscanCustom'),
            KeyboardButton(text='Vulners'),
            KeyboardButton(text='Vulscan')
        ],
        [
            KeyboardButton(text='В главное меню')
        ]
    ],
    resize_keyboard=True
)
