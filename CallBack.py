from aiogram import types
from deep_translator import GoogleTranslator
from pyaztro import Aztro

from config import _, bot
from keyboard import getHoroscopeKeyboard


async def horoscope_callback_handler(call: types.CallbackQuery):
    aztro_result = Aztro(sign=call.data).description
    user_leng=call.from_user.language_code

    if user_leng != "en": 
        aztro_result= GoogleTranslator('en',user_leng).translate(aztro_result)

    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id, text=call.data + ":\n" + (aztro_result) + "\n\n" + _("Which horoscope is interesting?"), reply_markup=getHoroscopeKeyboard())
    return

#Author: IPOleksenko
