import time

import config
import keyboards as kb
import texts
from async_tg_bot import *
from loader import db, qiwi

ADMIN = 'admin'
START = 'start'
BROADCAST = 'broadcast'
CANCEL = 'cancel'


def get_payment_url(bill_url: str) -> str:
    return f'https://anonym.to/?{bill_url}'


# === Admin


@on_command(ADMIN, user_id=config.ADMINS_IDS)
def admin():
    commands = [
        BotCommand(command=BROADCAST, description='Рассылка'),
        BotCommand(command=CANCEL, description='Отменить'),
    ]

    set_my_commands(commands, BotCommandScopeChat(chat_id=ctx.chat_id))
    send_message('Команды установлены')


# === Broadcast

@on_command(CANCEL, state='*')
def cancel():
    ctx.state = None
    send_message('Вы вышли из режима рассылки')


@on_command(BROADCAST, user_id=config.ADMINS_IDS)
def broadcast():
    ctx.state = BROADCAST
    send_message('Режим рассылки.\n\nОтправь сообщение для рассылки')


@on_message(state=BROADCAST)
def broadcast2():
    all_users = db.get_users()

    send_message(f'Начинаю рассылку (юзеров: {len(all_users)})')

    for row in all_users:
        user_id = row[0]

        try:
            copy_message(user_id)
        except errors.Error:
            db.set_active(user_id, False)
        else:
            db.set_active(user_id, True)
            time.sleep(0.1)

    send_message(f'Рассылка окончена,\n\n/{CANCEL} чтобы выйти из режима рассылки.')


# === Menu

@on_command(START)
def start():
    if not db.user_exists(ctx.user_id):
        db.add_user(ctx.user_id)
    else:
        db.set_active(ctx.user_id, True)
    send_message(texts.welcome, reply_markup=kb.main)


@on_text('👀 Обзор приватки')
def review():
    send_message(texts.review)


@on_text('💎 Выбрать тариф')
def tariffs():
    send_message('Выбери тариф, нажав на кнопку ниже👇🏻', reply_markup=kb.tariffs)


# === Tariffs

@on_data('tariff:1')
def tariff1():
    answer_callback_query()
    send_message(texts.tariff1_info, reply_markup=kb.pay1)


@on_data('tariff:2')
def tariff2():
    answer_callback_query()
    send_message(texts.tariff2_info, reply_markup=kb.pay2)


@on_data('tariff:3')
def tariff3():
    answer_callback_query()
    send_message(texts.tariff3_info, reply_markup=kb.pay3)


@on_data('tariff:4')
def tariff4():
    answer_callback_query()
    send_message(texts.tariff4_info, reply_markup=kb.pay4)


# === Pay

@on_data('pay:1')
def pay1():
    answer_callback_query()

    bill = qiwi.bill(amount=379, lifetime=30, comment='Оплата заказа')
    ctx.bill_id = bill.bill_id

    text = f'Для оплаты тарифа 🍪 2D Л0лbки, перейди по ссылке {get_payment_url(bill.pay_url)}'
    send_message(text, reply_markup=kb.check_payment1)


@on_data('pay:2')
def pay2():
    answer_callback_query()

    bill = qiwi.bill(amount=289, lifetime=30, comment='Оплата заказа')
    ctx.bill_id = bill.bill_id

    text = f'Для оплаты тарифа 📦 h3nta1 паки, перейди по ссылке {get_payment_url(bill)}'
    send_message(text, reply_markup=kb.check_payment2)


@on_data('pay:3')
def pay3():
    answer_callback_query()

    bill = qiwi.bill(amount=479, lifetime=30, comment='Оплата заказа')
    ctx.bill_id = bill.bill_id

    text = f'Для оплаты тарифа 🥵 3D L0ли, перейди по ссылке {get_payment_url(bill)}'
    send_message(text, reply_markup=kb.check_payment3)


@on_data('pay:4')
def pay4():
    answer_callback_query()

    bill = qiwi.bill(amount=789, lifetime=30, comment='Оплата заказа')
    ctx.bill_id = bill.bill_id

    text = f'Для оплаты тарифа 🔥 Всё сразу, перейди по ссылке {get_payment_url(bill)}'
    send_message(text, reply_markup=kb.check_payment4)


# === Check payment


@on_data('check_payment:1')
def check_payment1():
    status = qiwi.check(bill_id=ctx.bill_id).status
    # status = 'PAID'

    if status == 'PAID':
        link = create_chat_invite_link(chat_id=-1001558897531, member_limit=1)
        text = f'Спасибо за покупку 🥰\n\nСсылка на приватный канал c печеньками:\n\n{link.invite_link}'
        send_message(text)
    else:
        answer_callback_query('Платёж не найден', show_alert=True)


@on_data('check_payment:2')
def check_payment2():
    status = qiwi.check(bill_id=ctx.bill_id).status

    if status == 'PAID':
        link = create_chat_invite_link(chat_id=-1001695163553, member_limit=1)
        send_message(f'Спасибо за покупку 🥰\n\nСсылка на приватный канал с паками:\n\n{link.invite_link}')
    else:
        answer_callback_query('Платёж не найден', show_alert=True)


@on_data('check_payment:3')
def check_payment3():
    status = qiwi.check(bill_id=ctx.bill_id).status

    if status == 'PAID':
        link = create_chat_invite_link(chat_id=-1001703522776, member_limit=1)
        send_message(f'Спасибо за покупку 🥰\n\nСсылка на приватный канал:\n\n{link.invite_link}')
    else:
        answer_callback_query('Платёж не найден', show_alert=True)


@on_data('check_payment:4')
def check_payment4():
    status = qiwi.check(bill_id=ctx.bill_id).status

    if status == 'PAID':
        link1 = create_chat_invite_link(chat_id=-1001558897531, member_limit=1)
        link2 = create_chat_invite_link(chat_id=-1001695163553, member_limit=1)
        link3 = create_chat_invite_link(chat_id=-1001703522776, member_limit=1)
        links = f'{link1.invite_link}\n{link2.invite_link}\n{link3.invite_link}'
        send_message(f'Спасибо за покупку 🥰\n\nСсылки на все приватные каналы:\n\n{links}')
    else:
        answer_callback_query('Платёж не найден', show_alert=True)


def setup():
    pass
