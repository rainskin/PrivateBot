from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('💎 Выбрать тариф', '👀 Обзор приватки')

tariffs = InlineKeyboardMarkup(row_width=1)
tariffs.add(
    InlineKeyboardButton(text='🍪 2D Л0лbки', callback_data='tariff:1'),
    InlineKeyboardButton(text='📦 h3nta1 паки', callback_data='tariff:2'),
    InlineKeyboardButton(text='🥵 3D L0ли', callback_data='tariff:3'),
    InlineKeyboardButton(text='🔥 Всё сразу', callback_data='tariff:4'),
)

# === pay keyboards

pay1 = InlineKeyboardMarkup()
pay1.add(
    InlineKeyboardButton('💳 Оплатить', callback_data='pay:1')
)

pay2 = InlineKeyboardMarkup()
pay2.add(
    InlineKeyboardButton('💳 Оплатить', callback_data='pay:2')
)

pay3 = InlineKeyboardMarkup()
pay3.add(
    InlineKeyboardButton('💳 Оплатить', callback_data='pay:3')
)

pay4 = InlineKeyboardMarkup()
pay4.add(
    InlineKeyboardButton('💳 Оплатить', callback_data='pay:4')
)

# === check payment keyboards

check_payment1 = InlineKeyboardMarkup()
check_payment1.add(
    InlineKeyboardButton('⚙ Проверить оплату', callback_data='check_payment:1')
)

check_payment2 = InlineKeyboardMarkup()
check_payment2.add(
    InlineKeyboardButton('⚙ Проверить оплату', callback_data='check_payment:2')
)

check_payment3 = InlineKeyboardMarkup()
check_payment3.add(
    InlineKeyboardButton('⚙ Проверить оплату', callback_data='check_payment:3')
)

check_payment4 = InlineKeyboardMarkup()
check_payment4.add(
    InlineKeyboardButton('⚙ Проверить оплату', callback_data='check_payment:4')
)
