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



@dp.message_handler()
async def void(message):
    info_user(message)

    if message.text is not None:
        user_id=message.from_user.id
        user_firstname=message.from_user.first_name
        user_lastname=message.from_user.last_name
        user_username=message.from_user.username
        chat_id=message.chat.id
        datatime= datetime.now()

        Database_SQL.messageSave(message.text, user_id, user_firstname, user_lastname, user_username, chat_id, datatime)
    return

@dp.message_handler(content_types=['sticker'])
async def sticker(message):
    info_user(message)

    if message.sticker is not None:
        sticker_id=message.sticker.file_id
        file_unique_id=message.sticker.file_unique_id 
        name= message.sticker.set_name 
        emoji=message.sticker.emoji

        user_id=message.from_user.id
        user_firstname=message.from_user.first_name
        user_lastname=message.from_user.last_name
        user_username=message.from_user.username
        chat_id=message.chat.id
        datatime= datetime.now()

        Database_SQL.stickerSave(sticker_id, file_unique_id, name, emoji, user_id, user_firstname, user_lastname, user_username, chat_id, datatime)    
        return

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
    return

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

@dp.message_handler(content_types=['photo'])
async def photo(message):
    info_user(message)

    if message.photo is not None:
        document_id = message.photo[0].file_id

        photo_info = await bot.get_file(document_id)
        photo_id = photo_info.file_id
        photo_path = photo_info.file_path
        photo_size = photo_info.file_size
        photo_unique_id = photo_info.file_unique_id
        
        user_id=message.from_user.id
        user_firstname=message.from_user.first_name
        user_lastname=message.from_user.last_name
        user_username=message.from_user.username
        chat_id=message.chat.id
        datatime= datetime.now()

        Database_SQL.photoSeve(str(photo_info), photo_id, photo_path, photo_size, photo_unique_id, user_id, user_firstname, user_lastname, user_username, chat_id, datatime)

    return

@dp.message_handler(content_types=['video'])
async def video(message):
    info_user(message)

    if message.video is not None:
        document_id = message.video.file_id

        video_info = await bot.get_file(document_id)
        video_id = video_info.file_id
        video_path = video_info.file_path
        video_size = video_info.file_size
        video_unique_id = video_info.file_unique_id
        
        user_id=message.from_user.id
        user_firstname=message.from_user.first_name
        user_lastname=message.from_user.last_name
        user_username=message.from_user.username
        chat_id=message.chat.id
        datatime= datetime.now()

        Database_SQL.videoSeve(str(video_info), video_id, video_path, video_size, video_unique_id, user_id, user_firstname, user_lastname, user_username, chat_id, datatime)
    return

@dp.message_handler(content_types=['video_note'])
async def VideoNote(message):
    info_user(message)

    if message.video_note is not None:
        document_id = message.video_note.file_id
        VideoNote_info = await bot.get_file(document_id)
        VideoNote_id = VideoNote_info.file_id
        VideoNote_path = VideoNote_info.file_path
        VideoNote_size = VideoNote_info.file_size
        VideoNote_unique_id = VideoNote_info.file_unique_id
        
        user_id=message.from_user.id
        user_firstname=message.from_user.first_name
        user_lastname=message.from_user.last_name
        user_username=message.from_user.username
        chat_id=message.chat.id
        datatime= datetime.now()

        Database_SQL.VideoNoteSeve(str(VideoNote_info), VideoNote_id, VideoNote_path, VideoNote_size, VideoNote_unique_id, user_id, user_firstname, user_lastname, user_username, chat_id, datatime)
    return

@dp.message_handler(content_types=['document'])
async def document(message):
    info_user(message)

    if message.document is not None:
        document_id = message.document.file_id

        document_info = await bot.get_file(document_id)
        document_id = document_info.file_id
        document_path = document_info.file_path
        document_size = document_info.file_size
        document_unique_id = document_info.file_unique_id
        
        user_id=message.from_user.id
        user_firstname=message.from_user.first_name
        user_lastname=message.from_user.last_name
        user_username=message.from_user.username
        chat_id=message.chat.id
        datatime= datetime.now()

        Database_SQL.documentSeve(str(document_info), document_id, document_path, document_size, document_unique_id, user_id, user_firstname, user_lastname, user_username, chat_id, datatime)
    return

def voice(message, voice_info):
    voice_id = voice_info.file_id
    voice_path = voice_info.file_path
    voice_size = voice_info.file_size
    voice_unique_id = voice_info.file_unique_id
    
    user_id=message.from_user.id
    user_firstname=message.from_user.first_name
    user_lastname=message.from_user.last_name
    user_username=message.from_user.username
    chat_id=message.chat.id
    datatime= datetime.now()
    Database_SQL.voiceSeve(str(voice_info), voice_id, voice_path, voice_size, voice_unique_id, user_id, user_firstname, user_lastname, user_username, chat_id, datatime)

    return

###распознование текста в аудио###
@dp.message_handler(content_types=['voice'])
async def Voice_recognizer(message: types.Message):
    info_user(message)

    
    try:
        src_filename = 'Voice_user\\voice.ogg'    
        newFile = await bot.get_file(message.voice.file_id)
        if message.voice is not None:
            voice(message, newFile)
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
