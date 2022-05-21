from pyqiwip2p import QiwiP2P

import config
from db import Database

qiwi = QiwiP2P(auth_key=config.QIWI_KEY)

db = Database('database.db')
db.create_tables()
