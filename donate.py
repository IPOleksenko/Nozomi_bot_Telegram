from aiogram import types
from aiogram.types.message import ContentTypes
from config import bot, FOR_PAYMENTS, FOR_FORWARD
from SQL import db


# Setup shipping options
shipping_options = [
    types.ShippingOption(id='instant', title='WorldWide Teleporter').add(types.LabeledPrice('Teleporter', 1000)),
    types.ShippingOption(id='pickup', title='Local pickup').add(types.LabeledPrice('Pickup', 300)),
]

async def cmd_buy(message: types.Message):
    db.update_user(message)
    db.save_message(message)

    price=int(message.get_args().split()[0])*100 if message.get_args() and message.get_args().isalnum() else 100
    if price > 400000: price=400000

    await bot.forward_message(FOR_FORWARD, message.chat.id, message.message_id)
    await bot.send_invoice(message.chat.id, title='DONATE FOR ME❤️',
                           description='I love You❤️',
                           provider_token=FOR_PAYMENTS,
                           currency='usd',
                           prices=[types.LabeledPrice(label='DONATE', amount= price),],
                           payload='❤️')


async def shipping(shipping_query: types.ShippingQuery):
    await bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options, error_message='😭')


async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message="😭")


async def got_payment(message: types.Message):
    await bot.send_message(message.chat.id, '💋', parse_mode='Markdown')