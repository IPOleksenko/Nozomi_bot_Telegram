from aiogram import types
from deep_translator import GoogleTranslator
from pyaztro import Aztro

from config import _
from keyboard import getHoroscopeKeyboard


async def horoscope_callback_handler(call: types.CallbackQuery):
    aztro_result = Aztro(sign=call.data[1:]).description
    user_leng = call.from_user.language_code

    if user_leng != "en": 
        aztro_result= GoogleTranslator('en',user_leng).translate(aztro_result)

    result = call.data + ":\n" + (aztro_result) + "\n\n" + _("Which horoscope is interesting?")

    if result != call.message.text:
        return await call.message.edit_text(text=result, reply_markup=getHoroscopeKeyboard())

#Author: IPOleksenko
