import os
import logging
import asyncio

from bson import ObjectId
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types

from db import setup_db


load_dotenv()
API_TOKEN = os.environ.get('BOT_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)


async def start_command(message: types.Message):
    user = message.from_user.get_mention(as_html=True)
    await message.answer(
        f"Hello {user}.\nWrite here the address which you need to do shortened",
        parse_mode=types.ParseMode.HTML)


async def help_command(message: types.Message):
    user = message.from_user.get_mention(as_html=True)
    await message.answer(
        f"Dear, {user}.\nThis service will help you shorten the link to the resource",
        parse_mode=types.ParseMode.HTML)


async def get_user_url(message: types.Message):
    user_url_list = message.text.split('://')
    try:
        db = await setup_db()
        collection = db['shortener']
        obj_url = await collection.insert_one({'user_url': user_url_list[1], 'prefix': user_url_list[0]})
        user_id = str(obj_url.inserted_id)
        await message.answer(
            user_id
        )
    except Exception as error:
        await message.answer(
            str(error)
        )


async def send_user_url(message: types.Message):
    get_user_link_id = message.text
    try:
        db = await setup_db()
        collection = db['shortener']
        obj_url = await collection.find_one({'_id': ObjectId(get_user_link_id)})
        user_url = obj_url.get('user_url')
        prefix = obj_url.get('prefix', 'http')
        await message.answer(
            prefix + '://' + user_url
        )
    except Exception as error:
        await message.answer(
            str(error)
        )


async def main():
    bot = Bot(token=API_TOKEN)
    try:
        disp = Dispatcher(bot)
        disp.register_message_handler(start_command, commands={'start'})
        disp.register_message_handler(help_command, commands={'help'})
        disp.register_message_handler(get_user_url, regexp='http.+')
        disp.register_message_handler(send_user_url, regexp='^\w{24}$')
        await disp.start_polling()
    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())