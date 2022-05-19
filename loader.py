from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pyqiwip2p import QiwiP2P

import config
from db import Database

qiwi = QiwiP2P(auth_key=config.QIWI_KEY)
bot = Bot(token=config.BOT_TOKEN, disable_web_page_preview=True, parse_mode='html')

dp = Dispatcher(bot, storage=MemoryStorage())
db = Database('database.db')
db.create_tables()
