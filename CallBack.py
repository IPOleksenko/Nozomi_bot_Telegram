from aiogram import types
from pyaztro import Aztro

from deep_translator import GoogleTranslator

async def horoscope_callback_handler(call: types.CallbackQuery):
    aztro_result = Aztro(sign=call.data).description
    user_leng=call.from_user.language_code

    if user_leng != "en": 
        aztro_result=GoogleTranslator('en',user_leng).translate(aztro_result)
        

    if len(aztro_result)>200:
        aztro_result=aztro_result[:197]+"..."

    await call.answer((aztro_result), show_alert=True)
    return

#Author: IPOleksenko
