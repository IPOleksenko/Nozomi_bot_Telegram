import io
import json
import subprocess as sp
from datetime import datetime
from logging import DEBUG, basicConfig
from random import randrange

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ContentType, Message
from aiogram.utils import executor
from speech_recognition import AudioFile, Recognizer, UnknownValueError
from vosk import KaldiRecognizer

from config import CHAT_FOR_FORWARD, TOKEN, _, i18n, models
from keyboard import getHoroscopeKeyboard
from SQL import Database_SQL
from Weather_reaction import Weater_message
from CallBack import *

basicConfig(level=DEBUG)

r = Recognizer()
storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(i18n)


dp.register_callback_query_handler(horoscope_callback_handler)


def Examination(message):
    user_id=message.from_user.id
    chat_id=message.chat.id
    exam=Database_SQL.examination(user_id, chat_id)
    return exam



def info_user(message):
    user_id=message.from_user.id
    user_firstname=message.from_user.first_name
    user_lastname=message.from_user.last_name
    user_username=message.from_user.username
    chat_id=message.chat.id
    datatime= datetime.now()
    Lang = message.from_user.language_code
    
    Database_SQL.insert(user_id, user_firstname, user_lastname, user_username, chat_id, datatime, Lang)
    return
    
def message_save(message):
    if message.text is not None:
        user_id=message.from_user.id
        user_firstname=message.from_user.first_name
        user_lastname=message.from_user.last_name
        user_username=message.from_user.username
        chat_id=message.chat.id
        datatime= datetime.now()

        Database_SQL.messageSave(message.text, user_id, user_firstname, user_lastname, user_username, chat_id, datatime)

@dp.message_handler(content_types=[ContentType.NEW_CHAT_MEMBERS])
async def new_members_handler(message: Message):
    info_user(message)
    message_save(message)
    await bot.send_message((message.chat.id), _("Hello, I'm Nozomi! If you wanna start using me – send a /start in this chat"))
    return
    

@dp.message_handler(commands="start")
async def start(message: types.Message):
    info_user(message)
    message_save(message)

    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)

    await message.reply(_('help'))
    return

@dp.message_handler(commands="random")
async def random(message: types.Message):
    info_user(message)
    message_save(message)

    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)

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

@dp.message_handler(commands="weather")
async def weather(message: types.Message):
    info_user(message)
    message_save(message)

    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)

    arguments = message.get_args() 
    if arguments != '':
        await message.reply(Weater_message(arguments, message))    
    else:
        await message.reply(_('{You_didnt_enter_the_city}'))

@dp.message_handler(commands="horoscope")
async def horoscope(message: types.Message):
    info_user(message)
    message_save(message)

    args=message.get_args()
    if not args:
        await message.reply(_("Which horoscope is interesting?"), reply_markup=getHoroscopeKeyboard())
        return





@dp.message_handler(is_chat_admin=True, commands="MESSAGE")
@dp.message_handler(chat_type='private', commands="MESSAGE")
async def MESSAGE(message: types.Message):
    info_user(message)
    message_save(message)

    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)
        
    await bot.delete_message(message.chat.id, message.message_id)
    arguments = message.get_args()
    await bot.send_message(message.chat.id, arguments)
    return

@dp.message_handler(is_chat_admin=True, commands="KILLSTICKER")
@dp.message_handler(chat_type='private', commands="KILLSTICKER")
async def KILLSTICKER(message: types.Message):
    info_user(message)
    message_save(message)

    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)

    await message.delete()
    count = message.get_args()[0] if message.get_args() else ""
    count = int(count) if count.isdigit() else 1
    for _ in range(count):
        await message.answer_sticker(r"CAACAgIAAxkBAAEElfViavdiyQmJ3phUbRFDiLqkzBWAuwACvRcAAm7sUUuMK530YMmNUiQE")
    return

@dp.message_handler(is_chat_admin=True, commands="MYSTICKER")
@dp.message_handler(chat_type='private', commands="MYSTICKER")
async def MYSTICKER(message: types.Message):
    info_user(message)
    message_save(message)

    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)

    await message.delete()
    arguments = message.get_args()
    await message.answer_sticker(arguments)
    return

@dp.message_handler(is_chat_admin=True, commands="SENDBYID")
@dp.message_handler(chat_type='private', commands="SENDBYID")
async def SENDBYID(message: types.Message):
    info_user(message)
    message_save(message)
    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)

    args = message.get_args().split()

    reply = message.reply_to_message
    if not reply:
        await message.reply(_("SENDBYID_NOT_REPLY"))
        return

    if len(args) == 0:
        await message.reply(_("SENDBYID_NOT_ID"))
        return
        
    await message.delete()

    if len(args) == 1:
        await bot.copy_message(args[0], reply.chat.id, reply.message_id)
    elif len(args) >= 2:
        if args[1]=="False":
            await bot.copy_message(args[0], reply.chat.id, reply.message_id, disable_notification = False)
        elif args[1]=="True":
            await bot.copy_message(args[0], reply.chat.id, reply.message_id, disable_notification = True)
    return




@dp.message_handler(content_types="text")
async def text(message):
    info_user(message)
    message_save(message)

    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)
    return

@dp.message_handler(content_types="dice")
async def dice(message):
    info_user(message)

    if message.dice is not None:
        emoji=message.dice.emoji
        value=message.dice.value

        user_id=message.from_user.id
        user_firstname=message.from_user.first_name
        user_lastname=message.from_user.last_name
        user_username=message.from_user.username
        chat_id=message.chat.id
        datatime= datetime.now()

        Database_SQL.diceSave(emoji, value, user_id, user_firstname, user_lastname, user_username, chat_id, datatime)
    
    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)
    return

@dp.message_handler(content_types="animation")
async def animation(message):
    info_user(message)

    if message.animation is not None:
        animation_id = message.animation.file_id
        animation_info = await bot.get_file(animation_id)
        animation_id = animation_info.file_id
        animation_path = animation_info.file_path
        animation_size = animation_info.file_size
        animation_unique_id = animation_info.file_unique_id

        user_id=message.from_user.id
        user_firstname=message.from_user.first_name
        user_lastname=message.from_user.last_name
        user_username=message.from_user.username
        chat_id=message.chat.id
        datatime= datetime.now()
        Database_SQL.animationSave(str(animation_info), animation_id, animation_path, animation_size, animation_unique_id, user_id, user_firstname, user_lastname, user_username, chat_id, datatime)
    
    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)
    return

@dp.message_handler(content_types="poll")
async def poll(message):
    info_user(message)

    if message.poll is not None:
        poll_id=message.poll.id
        poll_question=message.poll.question
        poll_options=message.poll.options
        poll_correct_option_id=message.poll.correct_option_id
        poll_explanation=message.poll.explanation
        poll_is_anonymous=message.poll.is_anonymous

        user_id=message.from_user.id
        user_firstname=message.from_user.first_name
        user_lastname=message.from_user.last_name
        user_username=message.from_user.username
        chat_id=message.chat.id
        datatime= datetime.now()

        Database_SQL.pollSave(poll_id, poll_question, str(poll_options), poll_correct_option_id, poll_explanation, poll_is_anonymous, user_id, user_firstname, user_lastname, user_username, chat_id, datatime)
    
    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)
    return

@dp.message_handler(content_types="sticker")
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
        
        await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)
        return

@dp.message_handler(content_types="contact")
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

        Database_SQL.phoneSave(sender_user_id, phonenumber, user_id, first_name, last_name, vcard, datatime)
    
    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)
    return

@dp.message_handler(content_types="location")
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
        
        Database_SQL.locationSave(latitude, longitude, user_id, user_firstname, user_lastname, user_username, chat_id, datatime)
    
    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)
    return 

@dp.message_handler(content_types="photo")
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

        Database_SQL.photoSave(str(photo_info), photo_id, photo_path, photo_size, photo_unique_id, user_id, user_firstname, user_lastname, user_username, chat_id, datatime)
    
    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)
    return

@dp.message_handler(content_types="video")
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

        Database_SQL.videoSave(str(video_info), video_id, video_path, video_size, video_unique_id, user_id, user_firstname, user_lastname, user_username, chat_id, datatime)
    
    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)
    return

@dp.message_handler(content_types="video_note")
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

        Database_SQL.VideoNoteSave(str(VideoNote_info), VideoNote_id, VideoNote_path, VideoNote_size, VideoNote_unique_id, user_id, user_firstname, user_lastname, user_username, chat_id, datatime)
    
    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)
    return

@dp.message_handler(content_types="document")
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

        Database_SQL.documentSave(str(document_info), document_id, document_path, document_size, document_unique_id, user_id, user_firstname, user_lastname, user_username, chat_id, datatime)
    
    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)
    return

@dp.message_handler(content_types="audio")
async def audio(message):
    info_user(message)

    if message.audio is not None:
        file_id = message.audio.file_id

        audio_info = await bot.get_file(file_id)
        audio_id = audio_info.file_id
        audio_path = audio_info.file_path
        audio_size = audio_info.file_size
        audio_unique_id = audio_info.file_unique_id
        
        user_id=message.from_user.id
        user_firstname=message.from_user.first_name
        user_lastname=message.from_user.last_name
        user_username=message.from_user.username
        chat_id=message.chat.id
        datatime= datetime.now()
        
        Database_SQL.audioSave(str(audio_info), audio_id, audio_path, audio_size, audio_unique_id, user_id, user_firstname, user_lastname, user_username, chat_id, datatime)
    
    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)
    return

@dp.message_handler(content_types="voice")
async def Voice_recognizer(message: types.Message):
    info_user(message)

    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)
    
    voice_info = await bot.get_file(message.voice.file_id)
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

    Database_SQL.voiceSave(str(voice_info), voice_id, voice_path, voice_size, voice_unique_id, user_id, user_firstname, user_lastname, user_username, chat_id, datatime)


    result_text = ""
    bot_message = await message.reply(_("Think..."))

    lang = message.from_user.language_code
    lang = lang if lang in models.keys() else "en"
    kaldi = KaldiRecognizer(models[lang], 48000)

    voice = await message.voice.get_file()
    input = io.BytesIO()
    await voice.download(destination_file=input)

    cmd = [
        "ffmpeg",
        "-i",
        "pipe:",
        "-f",
        "wav",
        "-r",
        "16000",
        "-acodec",
        "pcm_s16le",
        "pipe:",
    ]
    proc = sp.Popen(cmd, stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.PIPE)
    result_ffmpeg = proc.communicate(input=input.read())[0]
    proc.wait()

    output = io.BytesIO(result_ffmpeg)

    if kaldi.AcceptWaveform(output.read()):
        result = kaldi.FinalResult()
        result_text = json.loads(result)["text"]

    if result_text == "":
        output.seek(0)
        with AudioFile(output) as source:
            r.adjust_for_ambient_noise(source, 0.5)
            r.energy_threshold = 300
            try:
                result_text = r.recognize_google(
                    r.record(source), language=message.from_user.language_code
                )
            except UnknownValueError:
                result_text = _("Failed to decrypt")

    return await bot_message.edit_text(result_text)


if __name__ == '__main__':
    Database_SQL.create_table()
    executor.start_polling(dp, skip_updates=True)
#Author: IPOleksenko
