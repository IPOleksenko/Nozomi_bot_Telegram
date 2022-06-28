from datetime import datetime
from logging import DEBUG, basicConfig

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ContentType, Message
from aiogram.utils import executor
from aiogram.utils.exceptions import FileIsTooBig
from aiogram.dispatcher.filters import BoundFilter
from speech_recognition import AudioFile, Recognizer, UnknownValueError, subprocess
from random import randrange

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

def info_user(message):
    user_id=message.from_user.id
    user_firstname=message.from_user.first_name
    user_lastname=message.from_user.last_name
    user_username=message.from_user.username
    chat_id=message.chat.id
    datatime= datetime.now()
    Lang = str(message.from_user.locale)
    
    Database_SQL.insert(user_id, user_firstname, user_lastname, user_username, chat_id, datatime, Lang)

@dp.message_handler(content_types=['contact'])
async def contact(message):
    info_user(message)

    if message.contact is not None:
        sender_user_id=message.from_user.id
        phonenumber= str(message.contact.phone_number)
        user_id = str(message.contact.user_id)
        first_name = str(message.contact.first_name)
        last_name = str(message.contact.last_name)
        vcard = str(message.contact.vcard)
        datatime= datetime.now()

        Database_SQL.phoneSeve(sender_user_id, phonenumber, user_id, first_name, last_name, vcard, datatime)

@dp.message_handler(content_types=['location'])
async def location(message):
    info_user(message)

    if message.location is not None:
        latitude = message.location.latitude
        longitude = message.location.longitude
        
        user_id=message.from_user.id
        user_firstname=message.from_user.first_name
        user_lastname=message.from_user.last_name
        user_username=message.from_user.username
        chat_id=message.chat.id
        datatime= datetime.now()
        
        Database_SQL.locationSeve(latitude, longitude, user_id, user_firstname, user_lastname, user_username, chat_id, datatime)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    info_user(message)

    await message.reply(_('help'))
    return

@dp.message_handler(commands=['random'])
async def process_start(message: types.Message):
    info_user(message)

    args = message.get_args().split()
    min = 1
    max = 10
    step = 1

    if len(args) == 1:
        max = int(args[0])
    elif len(args) >= 2:
        min = int(args[0])
        max = int(args[1]) 
    if len(args) >= 3:
        step = int(args[2])

    if max < min:
        min, max = max, min
    if step < 1:
        step = 1

    await message.reply(randrange(min, max, step))
    return 

@dp.message_handler(is_admin=True, commands=['MESSAGE'])
async def message(message: types.Message):
    info_user(message)
        
    await bot.delete_message(message.chat.id, message.message_id)
    arguments = message.get_args()
    await bot.send_message(message.chat.id, arguments)
    return

@dp.message_handler(is_admin=True, commands=['KILLSTICKER'])
async def KILLSTICKER(message: types.Message):
    info_user(message)

    await message.delete()
    count = message.get_args()[0] if message.get_args() else ""
    count = int(count) if count.isdigit() else 1
    for _ in range(count):
        await message.answer_sticker(r"CAACAgIAAxkBAAEElfViavdiyQmJ3phUbRFDiLqkzBWAuwACvRcAAm7sUUuMK530YMmNUiQE")
    return

@dp.message_handler(is_admin=True, commands=['MYSTICKER'])
async def MYSTICKER(message: types.Message):
    info_user(message)

    await message.delete()
    arguments = message.get_args()
    await message.answer_sticker(arguments)
    return

@dp.message_handler(commands=['weather'])
async def process_start(message: types.Message):
    info_user(message)

    arguments = message.get_args() 
    if arguments != '':
        await message.reply(Weater_message(arguments, message))    
    else:
        await message.reply(_('{You_didnt_enter_the_city}'))

###распознование текста в аудио###
@dp.message_handler(content_types=['voice'])
async def Voice_recognizer(message: types.Message):
    info_user(message)

    try:
        src_filename = 'Voice_user\\voice.ogg'    
        newFile = await bot.get_file(message.voice.file_id)
        await newFile.download(src_filename)       
    except FileIsTooBig:
        await message.reply(_('{big_file}'))
        return None
###Конвертация файла###
    dest_filename = f'Voice_user\\voice_output.wav'
    subprocess.run([f'ffmpeg\\bin\\ffmpeg.exe', '-i', src_filename, dest_filename, '-y'])
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
