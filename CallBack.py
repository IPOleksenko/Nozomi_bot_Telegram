from aiogram import types
from pyaztro import Aztro

from deep_translator import GoogleTranslator

async def horoscope_callback_handler(call: types.CallbackQuery):
    aztro_result = Aztro(sign=call.data).description
    user_leng=call.from_user.language_code

    if user_leng != "en": 
        await call.answer(GoogleTranslator('en',user_leng).translate(aztro_result), show_alert=True)
        return

    await call.answer(aztro_result, show_alert=True)
    return

#Author: IPOleksenko
