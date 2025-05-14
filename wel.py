import logging
import random
import asyncio
import aiohttp

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.middlewares import BaseMiddleware

# --- Bot Config ---
API_TOKEN = '7872751361:AAFX9seTY1upYixwLmerG8zcBFj6D8Pih0I'
OWNER_ID = 5260776753
CHANNEL_USERNAME = '@appifycreations'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

# --- Force Join Middleware ---
class ForceJoinMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        if message.chat.type != 'private':
            return
        try:
            member = await bot.get_chat_member(CHANNEL_USERNAME, message.from_user.id)
            if member.status in ['left', 'kicked']:
                raise Exception("Not joined")
        except:
            photo_url = "https://telegra.ph/file/1c9d7b48f5ae02bdf9b20.jpg"  # Replace with your image
            caption = (
                "🤖 *Welcome to raazxBot!*\n\n"
                "⚙️ _Your assistant for group welcome and management._\n\n"
                "🔒 Please join our official channel to continue.\n\n"
                "🆔 *Bot Owner:* [Raaz](https://t.me/appifycreations)"
            )
            buttons = InlineKeyboardMarkup(row_width=2).add(
                InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.strip('@')}"),
                InlineKeyboardButton("👤 Owner", url=f"https://t.me/{(await bot.get_chat(OWNER_ID)).username}")
            )
            await message.answer_photo(photo=photo_url, caption=caption, reply_markup=buttons, parse_mode="Markdown")
            raise Exception("User not in channel")

dp.middleware.setup(ForceJoinMiddleware())

# --- Start Command ---
@dp.message_handler(CommandStart())
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    keyboard = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.strip('@')}"),
        InlineKeyboardButton("👤 Owner", url=f"https://t.me/{(await bot.get_chat(OWNER_ID)).username}")
    )
    await message.answer(
        f"Hello {name}, welcome to **raazxBot**!",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

    await bot.send_message(
        OWNER_ID,
        f"🚀 *New user started bot!*\n\n"
        f"👤 Name: {message.from_user.full_name}\n"
        f"🔗 Username: @{message.from_user.username}\n"
        f"🆔 User ID: {message.from_user.id}",
        parse_mode="Markdown"
    )

# --- Group Join Welcome ---
@dp.chat_member_handler()
async def welcome_new_member(update: types.ChatMemberUpdated):
    if update.new_chat_member.user.is_bot:
        return
    if update.old_chat_member.status == 'left' and update.new_chat_member.status == 'member':
        name = update.new_chat_member.user.first_name
        user_id = update.new_chat_member.user.id
        image_url = await get_random_image()
        welcome_msg = f"Welcome, [{name}](tg://user?id={user_id})!"
        await bot.send_photo(update.chat.id, image_url, caption=welcome_msg, parse_mode='Markdown')

# --- Unsplash Random Image ---
async def get_random_image():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://source.unsplash.com/random/600x400/?welcome") as resp:
                return str(resp.url)
    except:
        return "https://source.unsplash.com/random/600x400"

# --- Run Bot ---
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
