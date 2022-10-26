from aiogram import types

from config import FOR_FORWARD, FOR_PAYMENTS, bot, _
from SQL import db

async def cmd_buy(message: types.Message):
    db.update_user(message)
    db.save_message(message)
    await bot.forward_message(FOR_FORWARD, message.chat.id, message.message_id)
    
    try:
        price=int(message.get_args().split()[0]) if message.get_args() and message.get_args().isalnum() else 1
        if price > 4000: price=4000
        if price <= 0: price=1    

        await bot.send_invoice(message.chat.id, title='Nozomi bot Telegram',
                               description='Donate for Nozomi❤️',
                               provider_token=FOR_PAYMENTS,
                               currency='USD',
                               prices=[types.LabeledPrice(label='DONATE', amount= price * 100),],
                               payload= f"[{message.date}] {message.from_user.username if message.from_user.username else message.from_user.first_name} [{message.from_user.id}] — ${price}",)
    except:
        return await message.reply(_("Sorry, an error has occurred😔"))

async def precheckout_callback(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message="😭")

async def got_payment(message: types.Message):
    await bot.send_message(message.chat.id, "🥹", parse_mode='Markdown')
    db.update_donate(message)