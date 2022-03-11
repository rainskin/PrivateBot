import datetime, threading, time
from pyqiwip2p import QiwiP2P
from aiogram.utils.exceptions import TelegramAPIError
from pyqiwip2p.types import QiwiCustomer, QiwiDatetime
from datetime import timedelta
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import text, bold, italic, code
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import Database
import asyncio
from config import TOKEN, QIWIKEY

p2p = QiwiP2P(auth_key=QIWIKEY)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database('database.db')
now = datetime.datetime.now()
BROADCAST_STATE = State('broadcast')


inline_btn_1 = InlineKeyboardButton('💳Оплатить', callback_data='pay1')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
inline_btn_3 = InlineKeyboardButton('💳Оплатить', callback_data='pay2')
inline_kb3 = InlineKeyboardMarkup().add(inline_btn_3)
inline_btn_2 = InlineKeyboardButton('⚙Проверить оплату', callback_data='check')
proverka = InlineKeyboardMarkup().add(inline_btn_2)
inline_btn_4 = InlineKeyboardButton('⚙Проверить оплату', callback_data='check2')
proverka2 = InlineKeyboardMarkup().add(inline_btn_4)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["💎Выбрать тариф", "👀Обзор приватки"]
    keyboard.add(*buttons)
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id)
        else:
            db.set_active(message.from_user.id, 1)
        await bot.send_message(message.from_user.id, "🥺Привет! Здесь ты можешь приобрести доступ в один из закрытых каналов"
                                                     "👉🏻👈🏻 \n\n Используй кнопки, чтобы выбрать тариф или ознакомиться подробнее"
                                                     , reply_markup=keyboard, disable_web_page_preview=True)


@dp.message_handler(commands='cancel', state='*')
async def broadcast2(msg: types.Message, state: FSMContext):
    await state.set_state(None)
    await msg.reply("Вы вышли из режима рассылки")


@dp.message_handler(commands='broadcast', user_id=[936845322])
async def broadcast(msg: types.Message):
    await msg.answer("Режим рассылки. \n \n Отправь сообщение для рассылки")
    await BROADCAST_STATE.set()

@dp.message_handler(content_types='any', state=BROADCAST_STATE)
async def broadcast2(msg: types.Message):
    USERS_IDS = db.get_users()
    for row in USERS_IDS:
        try:
            await msg.copy_to(row[0])
            await asyncio.sleep(0.1)
            if int(row[1]) != 1:
                db.set_active(row[0], 1)
        except TelegramAPIError:
            db.set_active(row[0], 0)

    await msg.answer("Рассылка окончена, \n\n /cancel чтобы выйти из режима рассылки.")


@dp.message_handler(lambda message: message.text == "👀Обзор приватки")
async def with_puree(message: types.Message):
    await message.answer(
        "Подробнее ознакомиться с контентом приваток можно по ссылке: \n\n https://telegra.ph/Obzor-privata--Review-on-a-private-channel-10-22")

@dp.message_handler(lambda message: message.text == "💎Выбрать тариф")  # ТАРИФЫ
async def without_puree(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="🎉Обычный доступ", callback_data="acces1"))
    keyboard.add(types.InlineKeyboardButton(text="🔥Премиум доступ", callback_data="acces2"))
    await message.answer("Выбери тариф, нажав на кнопку ниже👇🏻", reply_markup=keyboard)

@dp.callback_query_handler(text='acces1')
async def process_callback_acces1(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="💳Оплатить", callback_data="pay1"))
    try:
        p2p.reject(bill_id=new_bill.bill_id)
    except:
        pass
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, '*Тариф:* 🎉Обычный доступ \
                                                        \n*Стоимость:* 379 🇷🇺RUB \
                                                        \n*Срок действия*: бессрочно \
                                                        \n\n⭐️Доступ к приватному каналу с регулярными обновлениями *НАВСЕГДА*',
                           parse_mode="MarkdownV2", reply_markup=inline_kb1)

@dp.callback_query_handler(text='acces2')
async def process_callback_acces1(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="💳Оплатить", callback_data="pay2"))
    try:
        p2p.reject(bill_id=new_bill.bill_id)
    except:
        pass
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, '*Тариф:* 🔥Премиум доступ \
                                                        \n*Стоимость:* 589 🇷🇺RUB \
                                                        \n*Срок действия:* бессрочно \
                                                        \n\n⭐*Самый выгодный тариф* \n Доступ к приватному каналу с регулярными обновлениями *НАВСЕГДА* \
                                                        \n\n🎁Доступ к слитым пакам и материалам, на которые мы потратили уже около 25 000р', parse_mode="MarkdownV2", reply_markup=inline_kb3)

@dp.callback_query_handler(text='pay1')
async def process_callback_pay1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    global bill
    price = 1  # Цена которая будет запрашиваться у пользователя
    lifetime = 7  # Время действия ссылки
    comment = 'Оплата заказа'  # Комментарий к платежу, может быть абсолютно любым
    bill = p2p.bill(amount=price, lifetime=lifetime, comment=comment)  # Создаем счет
    link_oplata = bill.pay_url  # Получаем ссылку на оплату из нашего счета
    await bot.send_message(callback_query.from_user.id, text=f"Для оплаты, перейди по ссылке {link_oplata}", reply_markup=proverka)
    # x = threading.Thread(target=functionoplata) # Target - данный параметр принимает переменную, а в нашем варианте функцию которая будет проверять оплату. Args - аргументы, допустим для отправки сообщения.
    # x.start()  # Запуск потока


@dp.callback_query_handler(text='pay2')
async def process_callback_pay2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    global bill
    price = 2  # Цена которая будет запрашиваться у пользователя
    lifetime = 7  # Время действия ссылки
    comment = 'Оплата заказа'  # Комментарий к платежу, может быть абсолютно любым
    bill = p2p.bill(amount=price, lifetime=lifetime, comment=comment)  # Создаем счет
    link_oplata = bill.pay_url  # Получаем ссылку на оплату из нашего счета
    await bot.send_message(callback_query.from_user.id, text=f"Для ПРЕМИУМ оплаты, перейди по ссылке {link_oplata}",
                           reply_markup=proverka2)


@dp.callback_query_handler(text='check')
async def process_callback_check(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    oplata_time = datetime.datetime.now()  # Получаем текущее время
    datetime_delta = oplata_time + timedelta(minutes=7)  # Получаем разницу между датами.
    status = p2p.check(bill_id=bill.bill_id).status #Проверка статуса оплаты

    if status == 'PAID': #Проверка, на то - дошла ли оплата до бота. Вслучае положительного ответа, он выполняет данный if.
        await bot.send_message(callback_query.from_user.id,'Оплата дошла')
    if status == 'WAITING':
        await bot.send_message(callback_query.from_user.id, text=f'Платёж не найден, для оплаты, перейди по ссылке выше',reply_markup=proverka)
    elif datetime.datetime.now() > datetime_delta:
        await bot.send_message(callback_query.from_user.id,'Истекло время на оплату')
time.sleep(0.1) #Спим некое время, чтобы бот не крашнулся.

@dp.callback_query_handler(text='check2')
async def process_callback_check(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    oplata_time = datetime.datetime.now()  # Получаем текущее время
    datetime_delta = oplata_time + timedelta(minutes=7)  # Получаем разницу между датами.
    status = p2p.check(bill_id=bill.bill_id).status #Проверка статуса оплаты

    if status == 'PAID': #Проверка, на то - дошла ли оплата до бота. Вслучае положительного ответа, он выполняет данный if.
        await bot.send_message(callback_query.from_user.id,'Другая оплата дошла')
    if status == 'WAITING':
        await bot.send_message(callback_query.from_user.id, text=f'Платёж не найден, для оплаты, перейди по ссылке выше',reply_markup=proverka2)
    elif datetime.datetime.now() > datetime_delta:
        await bot.send_message(callback_query.from_user.id,'Истекло время на оплату')
time.sleep(0.1) #Спим некое время, чтобы бот не крашнулся.

# @dp.message_handler(commands=['start'])
# async def welcome(message: types.Message):
#     try:
#         p2p.reject(bill_id=new_bill.bill_id)
#     except:
#         pass
#     await message.answer('Вы хотите приобрести арбуз?\nДля приобретения пропишите /buywatermelon')


# @dp.message_handler(commands=['buywatermelon'])
# async def buy(message: types.Message):
#     global bill
#     price = 1 #Цена которая будет запрашиваться у пользователя
#     lifetime = 7 #Время действия ссылки
#     comment = 'Оплата заказа' #Комментарий к платежу, может быть абсолютно любым
#     bill = p2p.bill(amount=price, lifetime=lifetime, comment=comment) #Создаем счет
#     link_oplata = bill.pay_url #Получаем ссылку на оплату из нашего счета
#     await message.answer(f'Приветствуем!\nАрбуз стоит: {price} рублей\nСчет действителен 7 минут\nДля оплаты нажмите на данное слово: {link_oplata}')
#     x = threading.Thread(target=functionoplata, args=(message,)) #Target - данный параметр принимает переменную, а в нашем варианте функцию которая будет проверять оплату. Args - аргументы, допустим для отправки сообщения.
#     x.start() #Запуск потока

# async def functionoplata(message: types.Message): #Функция, ее можно создавать даже не асинхронной - ведь эта функция выполняется в потоке для пользователя.
#     oplata_time = datetime.datetime.now() #Получаем текущее время
#     datetime_delta = oplata_time + timedelta(minutes=7) #Получаем разницу между датами.
#     while True: #Создание цикла
#         status = p2p.check(bill_id=bill.bill_id).status #Проверка статуса оплаты
#         if status == 'PAID': #Проверка, на то - дошла ли оплата до бота. Вслучае положительного ответа, он выполняет данный if.
#             await message.answer('Оплата дошла до нас! Ауе')
#             break #Завершение цикла
#         elif datetime.datetime.now() > datetime_delta: #Делаем проверку, на время оплаты. То есть в случае неоплаты в течении 7-ми минут, цикл прекращается.
#             await message.answer('мужик, ты че не оплатил')
#             break #Завершение цикла
#     time.sleep(0.1) #Спим некое время, чтобы бот не крашнулся.
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True) #Запуск телеграм бота
