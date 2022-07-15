from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def getHoroscopeKeyboard():
    return InlineKeyboardMarkup(row_width = 2).add(
        InlineKeyboardButton(text='♈aries',            callback_data='♈Aries'), 
        InlineKeyboardButton(text='♉taurus',           callback_data='♉Taurus'),
        InlineKeyboardButton(text='♊gemini',           callback_data='♊Gemini'),
        InlineKeyboardButton(text='♋cancer',           callback_data='♋Cancer'),
        InlineKeyboardButton(text='♌leo',              callback_data='♌Leo'),
        InlineKeyboardButton(text='♍virgo',            callback_data='♍Virgo'),
        InlineKeyboardButton(text='♎libra',            callback_data='♎Libra'), 
        InlineKeyboardButton(text='♏scorpio',          callback_data='♏Scorpio'),
        InlineKeyboardButton(text='♐sagittarius',      callback_data='♐Sagittarius'),
        InlineKeyboardButton(text='♑capricorn',        callback_data='♑Capricorn'),
        InlineKeyboardButton(text='♒aquarius',         callback_data='♒Aquarius'),
        InlineKeyboardButton(text='♓pisces',           callback_data='♓Pisces'))

#Author: IPOleksenko
