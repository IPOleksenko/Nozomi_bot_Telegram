from pyaztro import Aztro
from aiogram import types

from config import bot, dp
from keyboard import Horoscope_cb, getHoroscopeKeyboard

dp.callback_query_handler(Horoscope_cb.filter(action='aries'))
async def Horoscope_cb_handler(query: types.CallbackQuery, callback_data: dict):
    await bot.edit_message_text(Aztro(sign='aries').description,
                                query.from_user.id,
                                query.message.message_id,
                                reply_markup=getHoroscopeKeyboard())

dp.callback_query_handler(Horoscope_cb.filter(action='taurus'))
async def Horoscope_cb_handler(query: types.CallbackQuery, callback_data: dict):
    await bot.edit_message_text(Aztro(sign='taurus').description,
                                query.from_user.id,
                                query.message.message_id,
                                reply_markup=getHoroscopeKeyboard())

dp.callback_query_handler(Horoscope_cb.filter(action='gemini'))
async def Horoscope_cb_handler(query: types.CallbackQuery, callback_data: dict):
    await bot.edit_message_text(Aztro(sign='gemini').description,
                                query.from_user.id,
                                query.message.message_id,
                                reply_markup=getHoroscopeKeyboard())

dp.callback_query_handler(Horoscope_cb.filter(action='cancer'))
async def Horoscope_cb_handler(query: types.CallbackQuery, callback_data: dict):
    await bot.edit_message_text(Aztro(sign='cancer').description,
                                query.from_user.id,
                                query.message.message_id,
                                reply_markup=getHoroscopeKeyboard())

dp.callback_query_handler(Horoscope_cb.filter(action='leo'))
async def Horoscope_cb_handler(query: types.CallbackQuery, callback_data: dict):
    await bot.edit_message_text(Aztro(sign='leo').description,
                                query.from_user.id,
                                query.message.message_id,
                                reply_markup=getHoroscopeKeyboard())

dp.callback_query_handler(Horoscope_cb.filter(action='virgo'))
async def Horoscope_cb_handler(query: types.CallbackQuery, callback_data: dict):
    await bot.edit_message_text(Aztro(sign='virgo').description,
                                query.from_user.id,
                                query.message.message_id,
                                reply_markup=getHoroscopeKeyboard())

dp.callback_query_handler(Horoscope_cb.filter(action='libra'))
async def Horoscope_cb_handler(query: types.CallbackQuery, callback_data: dict):
    await bot.edit_message_text(Aztro(sign='libra').description,
                                query.from_user.id,
                                query.message.message_id,
                                reply_markup=getHoroscopeKeyboard())

dp.callback_query_handler(Horoscope_cb.filter(action='scorpio'))
async def Horoscope_cb_handler(query: types.CallbackQuery, callback_data: dict):
    await bot.edit_message_text(Aztro(sign='scorpio').description,
                                query.from_user.id,
                                query.message.message_id,
                                reply_markup=getHoroscopeKeyboard())

dp.callback_query_handler(Horoscope_cb.filter(action='sagittarius'))
async def Horoscope_cb_handler(query: types.CallbackQuery, callback_data: dict):
    await bot.edit_message_text(Aztro(sign='sagittarius').description,
                                query.from_user.id,
                                query.message.message_id,
                                reply_markup=getHoroscopeKeyboard())

dp.callback_query_handler(Horoscope_cb.filter(action='capricorn'))
async def Horoscope_cb_handler(query: types.CallbackQuery, callback_data: dict):
    await bot.edit_message_text(Aztro(sign='capricorn').description,
                                query.from_user.id,
                                query.message.message_id,
                                reply_markup=getHoroscopeKeyboard())

dp.callback_query_handler(Horoscope_cb.filter(action='aquarius'))
async def Horoscope_cb_handler(query: types.CallbackQuery, callback_data: dict):
    await bot.edit_message_text(Aztro(sign='aquarius').description,
                                query.from_user.id,
                                query.message.message_id,
                                reply_markup=getHoroscopeKeyboard())

dp.callback_query_handler(Horoscope_cb.filter(action='pisces'))
async def Horoscope_cb_handler(query: types.CallbackQuery, callback_data: dict):
    await bot.edit_message_text(Aztro(sign='pisces').description,
                                query.from_user.id,
                                query.message.message_id,
                                reply_markup=getHoroscopeKeyboard())

#Author: IPOleksenko
