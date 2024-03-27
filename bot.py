import logging
import asyncio
import requests

from settings import API_TOKEN
from main import liq_photo
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Hello!')


@dp.message(Command('info'))
async def cmd_info(message: Message):
    await message.answer('Пришли фото и получишь измененное фото 0_0')


@dp.message(F.photo)
async def get_photo(message: Message):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    path = file.file_path
    link = f'https://api.telegram.org/file/bot{API_TOKEN}/{path}'

    with open('newfile.jpg', 'wb') as target:
        a = requests.get(link)
        target.write(a.content)
    liq_photo('newfile.jpg')
    res = FSInputFile('new_img.png')
    await message.answer_photo(res, caption='Измененное фото!')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit!')
