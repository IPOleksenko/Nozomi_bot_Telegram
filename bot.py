import io
import json
import subprocess as sp
from logging import DEBUG, basicConfig
from random import randrange

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ContentType, ContentTypes, Message
from aiogram.utils import executor
from aiogram.utils.executor import start_polling, start_webhook
from speech_recognition import AudioFile, Recognizer, UnknownValueError
from vosk import KaldiRecognizer

from CallBack import *
from config import (BOT_OWNER_USER, CHAT_FOR_FORWARD, DATABASE_URL, PORT,
                    TOKEN, WEBHOOK_HOST, _, i18n, models)
from keyboard import getHoroscopeKeyboard
from SQL import Database
from Weather_reaction import Weater_message

basicConfig(level=DEBUG)

r = Recognizer()
storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(i18n)
db = Database(dsn=DATABASE_URL)

dp.register_callback_query_handler(horoscope_callback_handler)


@dp.message_handler(content_types=[ContentType.NEW_CHAT_MEMBERS])
async def new_members_handler(message: Message):
    db.update_user(message)
    db.save_message(message)
    await bot.send_message((message.chat.id), _("Hello, I'm Nozomi! If you wanna start using me – send a /start in this chat"))
    return
    

@dp.message_handler(commands="start")
async def start(message: types.Message):
    db.update_user(message)
    db.save_message(message)

    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)

    await message.reply(_('help'))
    return

@dp.message_handler(commands="random")
async def random(message: types.Message):
    db.update_user(message)
    db.save_message(message)

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
    db.update_user(message)
    db.save_message(message)

    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)

    arguments = message.get_args() 
    if arguments != '':
        await message.reply(Weater_message(arguments, message))    
    else:
        await message.reply(_('{You_didnt_enter_the_city}'))

@dp.message_handler(commands="horoscope")
async def horoscope(message: types.Message):
    db.update_user(message)
    db.save_message(message)

    args=message.get_args()
    if not args:
        await message.reply(_("Which horoscope is interesting?"), reply_markup=getHoroscopeKeyboard())
        return


@dp.message_handler(is_chat_admin=True, commands="MESSAGE")
@dp.message_handler(chat_type='private', commands="MESSAGE")
async def MESSAGE(message: types.Message):
    db.update_user(message)
    db.save_message(message)

    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)
        
    await bot.delete_message(message.chat.id, message.message_id)
    arguments = message.get_args()
    await bot.send_message(message.chat.id, arguments)
    return

@dp.message_handler(is_chat_admin=True, commands="MYSTICKER")
@dp.message_handler(chat_type='private', commands="MYSTICKER")
async def MYSTICKER(message: types.Message):
    db.update_user(message)
    db.save_message(message)

    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)

    await message.delete()
    arguments = message.get_args()
    try:
        await message.answer_sticker(arguments)
    except:
        print("/nI was unable to send a sticker under the id: ", arguments, "\n")
    return

@dp.message_handler(chat_type='private', commands="SENDBYID")
async def SENDBYID(message: types.Message):
    db.update_user(message)
    db.save_message(message)
    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)

    args = message.get_args().split()

    reply = message.reply_to_message
    
    if str(message.from_user.id) == BOT_OWNER_USER:

        if not reply:
            await message.reply(_("SENDBYID_NOT_REPLY"))
            return

        if len(args) == 0:
            await message.reply(_("SENDBYID_NOT_ID"))
            return

        await message.delete()

        for x in args:
            try:
                await bot.copy_message(x, reply.chat.id, reply.message_id)
            except:
                print("\nI was unable to send a message to the user under the id: ", x, "\n")
        
    else:
        await message.reply(_("You are not my owner"))

@dp.message_handler(chat_type='private', commands="SENDALL")
async def SENDALL(message: types.Message):
    db.update_user(message)
    db.save_message(message)

    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)

    reply = message.reply_to_message

    if str(message.from_user.id) == BOT_OWNER_USER:
        if not reply:
            await message.reply(_("SENDBYID_NOT_REPLY"))
            return
        
        user_info = set(user.id for user in db.get_users())
        user_info = user_info.union(set(chat.id for chat in db.get_chats()))
        for id in user_info:
            try:
                await bot.copy_message(id, reply.chat.id, reply.message_id)
            except:
                print("\nI was unable to send a message to the user under the id: ", id, "\n")
            
    else:
        await message.reply(_("You are not my owner"))
    return


@dp.message_handler(content_types="voice")
async def Voice_recognizer(message: types.Message):
    db.update_user(message)
    db.save_message(message)

    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)
    

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


@dp.message_handler(content_types=ContentTypes.all())
async def handle_all(message: Message):
    db.update_user(message)
    db.save_message(message)
    await bot.forward_message(CHAT_FOR_FORWARD, message.chat.id, message.message_id)

    return True

async def on_startup(dp):
    await bot.set_webhook(f"{WEBHOOK_HOST}/bot{TOKEN}")

if __name__ == "__main__":
    if WEBHOOK_HOST is None:
        start_polling(dispatcher=dp, skip_updates=True)
    else:
        start_webhook(
            dispatcher=dp,
            webhook_path=f"/bot{TOKEN}",
            on_startup=on_startup,
            skip_updates=True,
            port=PORT,
        )
#Author: IPOleksenko
