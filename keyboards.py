from async_tg_bot.types import *

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='💎 Выбрать тариф'), KeyboardButton(text='👀 Обзор приватки')],
    ],
    resize_keyboard=True,
)

tariffs = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🍪 2D Л0лbки', callback_data='tariff:1')],
        [InlineKeyboardButton(text='📦 h3nta1 паки', callback_data='tariff:2')],
        [InlineKeyboardButton(text='🥵 3D L0ли', callback_data='tariff:3')],
        [InlineKeyboardButton(text='🔥 Всё сразу', callback_data='tariff:4')],
    ]
)

# === pay keyboards

pay1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='💳 Оплатить', callback_data='pay:1')]
    ]
)

pay2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='💳 Оплатить', callback_data='pay:2')]
    ]
)

pay3 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='💳 Оплатить', callback_data='pay:3')]
    ]
)

pay4 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='💳 Оплатить', callback_data='pay:4')]
    ]
)

# === check payment keyboards

check_payment1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='⚙ Проверить оплату', callback_data='check_payment:1')]
    ]
)
check_payment2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='⚙ Проверить оплату', callback_data='check_payment:2')]
    ]
)
check_payment3 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='⚙ Проверить оплату', callback_data='check_payment:3')]
    ]
)
check_payment4 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='⚙ Проверить оплату', callback_data='check_payment:4')]
    ]
)
