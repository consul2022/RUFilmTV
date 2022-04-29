import asyncio
from Constans import *
from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(BOT_TOKEN)
loop = asyncio.get_event_loop()  # асинхронный цикл

dp = Dispatcher(bot, loop, storage=MemoryStorage())


@dp.message_handler(content_type=['photo'])
async def get_photo_file_id(message: types.Message):
    print(message.photo[-1].file_id)


@dp.message_handler(content_type=['video'])
async def get_video_file_id(message: types.Message):
    print(message.video.file_id)
