from datetime import datetime
from logging import DEBUG, basicConfig

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ContentType, Message
from aiogram.utils import executor
from aiogram.utils.exceptions import FileIsTooBig
from aiogram.dispatcher.filters import BoundFilter
from speech_recognition import AudioFile, Recognizer, UnknownValueError, subprocess

from config import TOKEN, i18n, _
from SQL import Database_SQL
from Weather_reaction import Weater_message

r = Recognizer()
basicConfig(level=DEBUG)
storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(i18n)


def Examination(message):
    user_id=message.from_user.id
    chat_id=message.chat.id
    exam=Database_SQL.examination(user_id, chat_id)
    return exam


### Отклик при команде старт###
@dp.message_handler(content_types=[ContentType.NEW_CHAT_MEMBERS])
async def new_members_handler(message: Message):
    await bot.send_message((message.chat.id), _("Hello, I'm Nozomi! If you wanna start using me – send a /start in this chat"))

class MyFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin()
dp.filters_factory.bind(MyFilter)


@dp.message_handler(commands=['start'])
async def info_user(message: types.Message):
    ##########################################################
    user_id=message.from_user.id
    user_firstname=message.from_user.first_name
    user_lastname=message.from_user.last_name
    user_username=message.from_user.username
    if user_username == 'GroupAnonymousBot':
        await message.reply(_('{Anonimus_user}')+('?'))
        return
    chat_id=message.chat.id
    datatime= datetime.now()
    Lang = str(message.from_user.locale)
    ##########################################################
    Database_SQL.insert(user_id, user_firstname, user_lastname, user_username, chat_id, datatime, Lang)
    await message.reply(_('{WELCOME}'))


@dp.message_handler(commands=['random'])
async def process_start(message: types.Message):
    if Examination(message)=='None':
        await message.reply(_('{Firstly_send}'))
    
        return None

@dp.message_handler(is_admin=True, commands=['MESSAGE'])
async def message(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    arguments = message.get_args()
    if Examination(message)=='None':
        await message.reply(_('{Firstly_send}'))
        return None
    await bot.send_message(message.chat.id, arguments)
    return

@dp.message_handler(is_admin=True, commands=['KILLSTICKER'])
async def KILLSTICKER(message: types.Message):
    await message.delete()
    if Examination(message)=='None':
        await message.reply(_('{Firstly_send}'))
        return None
    count = message.get_args()[0] if message.get_args() else ""
    count = int(count) if count.isdigit() else 1
    for _ in range(count):
        await message.answer_sticker(r"CAACAgIAAxkBAAEElfViavdiyQmJ3phUbRFDiLqkzBWAuwACvRcAAm7sUUuMK530YMmNUiQE")
    return

@dp.message_handler(is_admin=True, commands=['MYSTICKER'])
async def MYSTICKER(message: types.Message):
    await message.delete()
    if Examination(message)=='None':
        await message.reply(_('{Firstly_send}'))
        return None
    arguments = message.get_args()
    await message.answer_sticker(arguments)
    return

@dp.message_handler(commands=['weather'])
async def process_start(message: types.Message):
    arguments = message.get_args()
    if Examination(message)=='None':
        await message.reply(_('{Firstly_send}'))
        return None  
    if arguments != '':
        await message.reply(Weater_message(arguments, message))    
    else:
        await message.reply(_('{You_didnt_enter_the_city}'))

###распознование текста в аудио###
@dp.message_handler(content_types=['voice'])
async def Voice_recognizer(message: types.Message):
    if Examination(message)=='None':
        await message.reply(_('{Firstly_send}'))
        return None  
    try:
        src_filename = 'Nozomi_bot_Telegram\\Voice_user\\voice.ogg'    
        newFile = await bot.get_file(message.voice.file_id)
        await newFile.download(src_filename)       
    except FileIsTooBig:
        await message.reply(_('{big_file}'))
        return None
###Конвертация файла###
    dest_filename = f'Nozomi_bot_Telegram\\Voice_user\\voice_output.wav'
    subprocess.run([f'Nozomi_bot_Telegram\\ffmpeg\\bin\\ffmpeg.exe', '-i', src_filename, dest_filename, '-y'])
###Распознование слов###
    with AudioFile(dest_filename) as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        r.energy_threshold = 300
        try:
            text = r.recognize_google(r.record(source), language = str(message.from_user.locale))
            text = ''.join(text)
            await message.reply(_('{I_heard}')+(':')+(f'\n"{text}"'))
        except UnknownValueError:
            await message.reply(_('{BAKA}')+('.'))
if __name__ == '__main__':
    Database_SQL.create_table()
    executor.start_polling(dp, skip_updates=True)
#Author: IPOleksenko
