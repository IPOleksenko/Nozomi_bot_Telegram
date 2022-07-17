import io
import json
import subprocess as sp
from logging import DEBUG, basicConfig, error
from random import randrange

from aiogram import Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ContentType, ContentTypes, Message
from aiogram.utils.executor import start_polling, start_webhook
from speech_recognition import AudioFile, Recognizer, UnknownValueError
from vosk import KaldiRecognizer

from call_back import *
from config import (BOT_OWNER_USER, FOR_FORWARD, PORT, TOKEN, WEBHOOK_HOST, _,
                    i18n, models)
from donate import *
from keyboard import getHoroscopeKeyboard
from middleware import *
from SQL import db
from Weather_reaction import Weater_message

basicConfig(level=DEBUG)

r = Recognizer()
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


dp.middleware.setup(i18n)
dp.middleware.setup(MediaGroupMiddleware())

dp.register_callback_query_handler(horoscope_callback_handler)
dp.register_message_handler(cmd_buy, commands="donate")
dp.register_callback_query_handler(shipping, lambda query: True)
dp.register_callback_query_handler(checkout, lambda query: True)
dp.register_message_handler(got_payment, content_types=ContentTypes.SUCCESSFUL_PAYMENT)


@dp.message_handler(content_types=[ContentType.NEW_CHAT_MEMBERS])
async def new_members_handler(message: Message):
    db.update_user(message)
    db.save_message(message)
    await bot.forward_message(FOR_FORWARD, message.chat.id, message.message_id)

    if str(message.from_user.id) == BOT_OWNER_USER:
        try:
            return await message.chat.promote(
			user_id=message.from_user.id,
            is_anonymous=False,
			can_change_info=True,
            can_post_messages=True,
            can_edit_messages=True,
            can_delete_messages=True,
            can_invite_users=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_promote_members=True,)
        except:
            return error("\nI can't make it an admin(\n")

    return await bot.send_message((message.chat.id), _("Hello, I'm Nozomi! If you wanna start using me – send a /start in this chat"))

@dp.message_handler(commands="start")
async def start(message: types.Message):
    db.update_user(message)
    db.save_message(message)
    await bot.forward_message(FOR_FORWARD, message.chat.id, message.message_id)

    return await message.reply(_('help'))


@dp.message_handler(commands="random")
async def random(message: types.Message):
    db.update_user(message)
    db.save_message(message)
    await bot.forward_message(FOR_FORWARD, message.chat.id, message.message_id)

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

    return await message.reply(randrange(min, max, step)) 

@dp.message_handler(commands="weather")
async def weather(message: types.Message):
    db.update_user(message)
    db.save_message(message)
    await bot.forward_message(FOR_FORWARD, message.chat.id, message.message_id)

    arguments = message.get_args() 
    if arguments != '':
        return await message.reply(Weater_message(arguments, message))    
    else:
        return await message.reply(_('{You_didnt_enter_the_city}'))

@dp.message_handler(commands="horoscope")
async def horoscope(message: types.Message):
    db.update_user(message)
    db.save_message(message)
    await bot.forward_message(FOR_FORWARD, message.chat.id, message.message_id)

    args=message.get_args()
    if not args:
        return await message.reply(_("Which horoscope is interesting?"), reply_markup=getHoroscopeKeyboard())


@dp.message_handler(is_chat_admin=True, commands="MESSAGE")
@dp.message_handler(chat_type='private', commands="MESSAGE")
async def MESSAGE(message: types.Message):
    db.update_user(message)
    db.save_message(message)
    await bot.forward_message(FOR_FORWARD, message.chat.id, message.message_id)
    await bot.delete_message(message.chat.id, message.message_id)
    
    arguments = message.get_args()
    
    try:
        return await bot.send_message(message.chat.id, arguments)
    except:
        return error("\nI couldn't send a message\n")

@dp.message_handler(chat_type='private', commands="SENDBYID")
async def SENDBYID(message: types.Message):
    db.update_user(message)
    db.save_message(message)
    await bot.forward_message(FOR_FORWARD, message.chat.id, message.message_id)

    args = message.get_args().split()

    reply = message.reply_to_message
    
    if str(message.from_user.id) == BOT_OWNER_USER:

        if not reply:
            return await message.reply(_("SENDBYID_NOT_REPLY"))
            

        if len(args) == 0:
            return await message.reply(_("SENDBYID_NOT_ID"))
            

        for x in args:
            try:
                return await bot.copy_message(x, reply.chat.id, reply.message_id)
            except:
                return error("\nI was unable to send a message to the user under the id: {x}\n".format(x=x))
        
    else:
        return await message.reply(_("You are not my owner"))

@dp.message_handler(chat_type='private', commands="SENDALL")
async def SENDALL(message: types.Message):
    db.update_user(message)
    db.save_message(message)
    await bot.forward_message(FOR_FORWARD, message.chat.id, message.message_id)
    reply = message.reply_to_message

    if str(message.from_user.id) == BOT_OWNER_USER:
        if not reply:
            return await message.reply(_("SENDBYID_NOT_REPLY"))
            
        
        chat_info = set(user.id for user in db.get_chats())

        for id in chat_info:
            try:
                await bot.copy_message(id, reply.chat.id, reply.message_id)
            except:
                return error("\nI was unable to send a message to the user under the id: {id}\n".format(id=id))
            
    else:
        return await message.reply(_("You are not my owner"))

@dp.message_handler(commands="DELETE")
async def DELETE(message: types.Message):
    db.update_user(message)
    db.save_message(message)
    await bot.forward_message(FOR_FORWARD, message.chat.id, message.message_id)

    args = (message.get_args()).split()
    reply = message.reply_to_message
    
    await bot.delete_message(message.chat.id, message.message_id)
    
    if str(message.from_user.id) == BOT_OWNER_USER:
        try:
            if len(args) < 2:
                return await bot.delete_message(reply.chat.id, reply.message_id)
            else:
                return await bot.delete_message(args[0], args[1])
        except:
            return error("\nCan't delete this post or you didn't say what to delete(\n")

@dp.message_handler(commands="BAN")
async def BAN(message: types.Message):
    db.update_user(message)
    db.save_message(message)
    await bot.forward_message(FOR_FORWARD, message.chat.id, message.message_id)

    await bot.delete_message(message.chat.id, message.message_id)

    args = (message.get_args()).split()
    
    if str(message.from_user.id) == BOT_OWNER_USER:
        try:
            if len(args) < 2:
                reply = message.reply_to_message
                return await bot.ban_chat_member(reply.chat.id, reply.from_user.id)
            else:
                return await bot.ban_chat_member(args[0], args[1])
        except:
            return error("\nI was unable to block this user\n")

@dp.message_handler(commands="UNBAN")
async def UNBAN(message: types.Message):
    db.update_user(message)
    db.save_message(message)
    await bot.forward_message(FOR_FORWARD, message.chat.id, message.message_id)
    
    await bot.delete_message(message.chat.id, message.message_id)

    args = (message.get_args()).split()
    
    if str(message.from_user.id) == BOT_OWNER_USER:
        try:
            if len(args) < 2:
                reply = message.reply_to_message
                return await bot.unban_chat_member(reply.chat.id, reply.from_user.id)
            else:
                return await bot.unban_chat_member(args[0], args[1])
        except:
            return error("\nI was unable to unblock this user\n")


@dp.message_handler(content_types="voice")
async def Voice_recognizer(message: types.Message):
    db.update_user(message)
    db.save_message(message)

    await bot.forward_message(FOR_FORWARD, message.chat.id, message.message_id)
    

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
    

@dp.message_handler(is_media_group=True, content_types=types.ContentType.ANY)
async def handle_all_media(message: types.Message, media_album: list[types.Message]):
    media_group = types.MediaGroup()

    for media in media_album:
        db.update_user(media)
        db.save_message(media)

        if media.photo:
            file_id = media.photo[-1].file_id
        else:
            file_id = media[media.content_type].file_id

        try:
            media_group.attach({"media": file_id, "type": media.content_type})
        except ValueError:
            return None
    return await bot.send_media_group(FOR_FORWARD, media_group)
        
@dp.message_handler(content_types=types.ContentType.ANY)
async def handle_all(message: Message):
    db.update_user(message)
    db.save_message(message)
    return await bot.forward_message(FOR_FORWARD, message.chat.id, message.message_id)


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
