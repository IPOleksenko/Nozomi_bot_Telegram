import asyncio

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

class MediaGroupMiddleware(BaseMiddleware):
    media_album: dict = {}

    def __init__(self, latency: int | float = 0.01):
        self.latency = latency
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        if not message.media_group_id:
            return

        try:
            self.media_album[message.media_group_id].append(message)
            raise CancelHandler()
        except KeyError:
            self.media_album[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            message.conf["is_last"] = True
            data["media_album"] = self.media_album[message.media_group_id]

    async def on_post_process_message(self, message: types.Message, result: dict, data: dict):
        if message.media_group_id and message.conf.get("is_last"):
            del self.media_album[message.media_group_id]