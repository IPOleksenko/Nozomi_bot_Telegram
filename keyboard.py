from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def getHoroscopeKeyboard():
    return InlineKeyboardMarkup(row_width = 2).add(
        InlineKeyboardButton(text='♈aries',            callback_data='aries'), 
        InlineKeyboardButton(text='♉taurus',           callback_data='taurus'),
        InlineKeyboardButton(text='♊gemini',           callback_data='gemini'),
        InlineKeyboardButton(text='♋cancer',           callback_data='cancer'),
        InlineKeyboardButton(text='♌leo',              callback_data='leo'),
        InlineKeyboardButton(text='♍virgo',            callback_data='virgo'),
        InlineKeyboardButton(text='♎libra',            callback_data='libra'), 
        InlineKeyboardButton(text='♏scorpio',          callback_data='scorpio'),
        InlineKeyboardButton(text='♐sagittarius',      callback_data='sagittarius'),
        InlineKeyboardButton(text='♑capricorn',        callback_data='capricorn'),
        InlineKeyboardButton(text='♒aquarius',         callback_data='aquarius'),
        InlineKeyboardButton(text='♓pisces',           callback_data='pisces'))

#Author: IPOleksenko