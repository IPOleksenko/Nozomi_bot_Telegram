from os import getenv
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from pathlib import Path

TOKEN = getenv("TOKEN")
OW_API = getenv("OW_API")
DATABASE_URL = getenv("DATABASE_URL")

CHAT_FOR_FORWARD = getenv("CHAT_FOR_FORWARD")

I18N_DOMAIN = 'bot'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'
i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)
_ = i18n.gettext
#Author: IPOleksenko