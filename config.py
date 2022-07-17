from os import getenv
from pathlib import Path

from aiogram import Bot
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from vosk import Model

TOKEN = getenv("TOKEN")
bot = Bot(TOKEN)
OW_API = getenv("OW_API")
DATABASE_URL = getenv("DATABASE_URL")
FOR_PAYMENTS = getenv("FOR_PAYMENTS")
FOR_FORWARD = getenv("FOR_FORWARD")

BOT_OWNER_USER = getenv("BOT_OWNER_USER")

WEBHOOK_HOST = getenv("WEBHOOK_HOST")
PORT = getenv("PORT", 5555)

I18N_DOMAIN = 'bot'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'
i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)
_ = i18n.gettext

models = {
    "en": Model("models/en"),
    "ru": Model("models/ru")
}

#Author: IPOleksenko
