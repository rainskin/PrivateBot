import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.types import BotCommand
from aiogram.utils.exceptions import TelegramAPIError
from pyqiwip2p.p2p_types import Bill

import config
import keyboards as kb
import texts
from loader import dp, db, qiwi

BROADCAST_STATE = State('broadcast')

START = 'start'
BROADCAST = 'broadcast'
CANCEL = 'cancel'


def get_payment_url(bill: Bill) -> str:
    return f'https://anonym.to/?{bill.pay_url}'


@dp.message_handler(commands='admin', user_id=config.ADMINS_IDS)
async def admin(msg: types.Message):
    commands = [
        BotCommand(BROADCAST, 'Рассылка'),
        BotCommand(CANCEL, 'Отменить'),
    ]

    await dp.bot.set_my_commands(commands, types.BotCommandScopeChat(msg.from_user.id))
    await msg.answer('Команды установлены')


@dp.message_handler(commands=START, chat_type='private')
async def start(msg: types.Message):
    if not db.user_exists(msg.from_user.id):
        db.add_user(msg.from_user.id)
    else:
        db.set_active(msg.from_user.id, 1)
    await msg.answer(texts.welcome, reply_markup=kb.main)


@dp.message_handler(commands=BROADCAST, user_id=config.ADMINS_IDS)
async def broadcast(msg: types.Message):
    await BROADCAST_STATE.set()
    await msg.answer('Режим рассылки.\n\nОтправь сообщение для рассылки')


@dp.message_handler(commands=CANCEL, state='*')
async def cancel(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.reply('Вы вышли из режима рассылки')


@dp.message_handler(content_types='any', state=BROADCAST_STATE)
async def broadcast2(msg: types.Message):
    all_users = db.get_users()

    await msg.answer(f'Начинаю рассылку (юзеров: {len(all_users)})')

    for row in all_users:
        user_id = row[0]

        try:
            await msg.copy_to(user_id)
        except TelegramAPIError:
            db.set_active(user_id, False)
        else:
            db.set_active(user_id, True)
            await asyncio.sleep(0.1)

    await msg.answer(f'Рассылка окончена,\n\n/{CANCEL} чтобы выйти из режима рассылки.')


@dp.message_handler(text='👀 Обзор приватки')
async def review(message: types.Message):
    await message.answer(texts.review)


@dp.message_handler(text='💎 Выбрать тариф')
async def tariffs(message: types.Message):
    await message.answer('Выбери тариф, нажав на кнопку ниже👇🏻', reply_markup=kb.tariffs)


@dp.callback_query_handler(text='tariff:1')
async def tariff1(query: types.CallbackQuery):
    await query.answer()
    await query.message.answer(texts.tariff1_info, reply_markup=kb.pay1)


@dp.callback_query_handler(text='tariff:2')
async def tariff2(query: types.CallbackQuery):
    await query.answer()
    await query.message.answer(texts.tariff2_info, reply_markup=kb.pay2)


@dp.callback_query_handler(text='tariff:3')
async def tariff3(query: types.CallbackQuery):
    await query.answer()
    await query.message.answer(texts.tariff3_info, reply_markup=kb.pay3)


@dp.callback_query_handler(text='tariff:4')
async def tariff4(query: types.CallbackQuery):
    await query.answer()
    await query.message.answer(texts.tariff4_info, reply_markup=kb.pay4)


@dp.callback_query_handler(text='pay:1')
async def pay1(query: types.CallbackQuery, state: FSMContext):
    await query.answer()

    bill = qiwi.bill(amount=379, lifetime=30, comment='Оплата заказа')
    await state.update_data(bill_id=bill.bill_id)

    text = f'Для оплаты тарифа 🍪 2D Л0лbки, перейди по ссылке {get_payment_url(bill)}'
    await query.message.answer(text, reply_markup=kb.check_payment1)


@dp.callback_query_handler(text='pay:2')
async def pay2(query: types.CallbackQuery, state: FSMContext):
    await query.answer()

    bill = qiwi.bill(amount=289, lifetime=30, comment='Оплата заказа')
    await state.update_data(bill_id=bill.bill_id)

    text = f'Для оплаты тарифа 📦 h3nta1 паки, перейди по ссылке {get_payment_url(bill)}'
    await query.message.answer(text, reply_markup=kb.check_payment2)


@dp.callback_query_handler(text='pay:3')
async def pay3(query: types.CallbackQuery, state: FSMContext):
    await query.answer()

    bill = qiwi.bill(amount=479, lifetime=30, comment='Оплата заказа')
    await state.update_data(bill_id=bill.bill_id)

    text = f'Для оплаты тарифа 🥵 3D L0ли, перейди по ссылке {get_payment_url(bill)}'
    await query.message.answer(text, reply_markup=kb.check_payment3)


@dp.callback_query_handler(text='pay:4')
async def pay4(query: types.CallbackQuery, state: FSMContext):
    await query.answer()

    bill = qiwi.bill(amount=789, lifetime=30, comment='Оплата заказа')
    await state.update_data(bill_id=bill.bill_id)

    text = f'Для оплаты тарифа 🔥 Всё сразу, перейди по ссылке {get_payment_url(bill)}'
    await query.message.answer(text, reply_markup=kb.check_payment4)


@dp.callback_query_handler(text='check_payment:1')
async def check_payment1(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    bill_id: str = data['bill_id']

    status = qiwi.check(bill_id=bill_id).status

    if status == 'PAID':
        link = await dp.bot.create_chat_invite_link(chat_id=-1001558897531, member_limit=1)
        text = f'Спасибо за покупку 🥰\n\nСсылка на приватный канал c печеньками:\n\n{link.invite_link}'
        await query.message.answer(text)
    else:
        await query.answer(text=f'Платёж не найден', show_alert=True)


@dp.callback_query_handler(text='check_payment:2')
async def check_payment2(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    bill_id: str = data['bill_id']

    status = qiwi.check(bill_id=bill_id).status

    if status == 'PAID':
        link = await dp.bot.create_chat_invite_link(chat_id=-1001695163553, member_limit=1)
        text = f'Спасибо за покупку 🥰\n\nСсылка на приватный канал с паками:\n\n{link.invite_link}'
        await query.message.answer(text)
    else:
        await query.answer(text=f'Платёж не найден', show_alert=True)


@dp.callback_query_handler(text='check_payment:3')
async def check_payment3(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    bill_id: str = data['bill_id']

    status = qiwi.check(bill_id=bill_id).status

    if status == 'PAID':
        link = await dp.bot.create_chat_invite_link(chat_id=-1001703522776, member_limit=1)
        text = f'Спасибо за покупку 🥰\n\nСсылка на приватный канал:\n\n{link.invite_link}'
        await query.message.answer(text)
    else:
        await query.answer(text=f'Платёж не найден', show_alert=True)


@dp.callback_query_handler(text='check_payment:4')
async def check_payment4(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    bill_id: str = data['bill_id']

    status = qiwi.check(bill_id=bill_id).status
    # status = 'PAID'

    if status == 'PAID':
        link1 = await dp.bot.create_chat_invite_link(chat_id=-1001558897531, member_limit=1)
        link2 = await dp.bot.create_chat_invite_link(chat_id=-1001695163553, member_limit=1)
        link3 = await dp.bot.create_chat_invite_link(chat_id=-1001703522776, member_limit=1)

        links = f'{link1.invite_link}\n{link2.invite_link}\n{link3.invite_link}'

        text = f'Спасибо за покупку 🥰\n\nСсылки на все приватные каналы:\n\n{links}'
        await query.message.answer(text)
    else:
        await query.answer(text=f'Платёж не найден', show_alert=True)
