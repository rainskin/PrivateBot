import logging

import handlers
from async_tg_bot import run

logging.basicConfig(level=20, filemode='a', filename='.log')

handlers.setup()

run(
    parse_mode='html',
    disable_web_page_preview=True,
)
