from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

Horoscope_cb = CallbackData('aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces')

def getHoroscopeKeyboard():
    return InlineKeyboardMarkup(row_width = 2).add(
        InlineKeyboardButton(text='aries♈',            callback_data=Horoscope_cb.new(action='aries')), 
        InlineKeyboardButton(text='taurus♉',           callback_data=Horoscope_cb.new(action='taurus')),
        InlineKeyboardButton(text='gemini♊',           callback_data=Horoscope_cb.new(action='gemini')),
        InlineKeyboardButton(text='cancer♋',           callback_data=Horoscope_cb.new(action='cancer')),
        InlineKeyboardButton(text='leo♌',              callback_data=Horoscope_cb.new(action='leo')),
        InlineKeyboardButton(text='virgo♍',            callback_data=Horoscope_cb.new(action='virgo')),
        InlineKeyboardButton(text='libra♎',            callback_data=Horoscope_cb.new(action='libra')), 
        InlineKeyboardButton(text='scorpio♏',          callback_data=Horoscope_cb.new(action='scorpio')),
        InlineKeyboardButton(text='sagittarius♐',      callback_data=Horoscope_cb.new(action='sagittarius')),
        InlineKeyboardButton(text='capricorn♑',        callback_data=Horoscope_cb.new(action='capricorn')),
        InlineKeyboardButton(text='aquarius♒',         callback_data=Horoscope_cb.new(action='aquarius')),
        InlineKeyboardButton(text='pisces♓',           callback_data=Horoscope_cb.new(action='pisces')))

#Author: IPOleksenko