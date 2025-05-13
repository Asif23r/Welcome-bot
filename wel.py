import logging import random import asyncio from aiogram import Bot, Dispatcher, types from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup from aiogram.utils import executor from aiogram.dispatcher.filters import CommandStart from aiogram.dispatcher.middlewares import BaseMiddleware import aiohttp

API_TOKEN = '7872751361:AAFX9seTY1upYixwLmerG8zcBFj6D8Pih0I' OWNER_ID = 5260776753 CHANNEL_USERNAME = '@appifycreations'

bot = Bot(token=API_TOKEN) dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

--- Force Join Middleware ---

class ForceJoinMiddleware(BaseMiddleware): async def on_pre_process_message(self, message: types.Message, data: dict): if message.chat.type != 'private': return try: member = await bot.get_chat_member(CHANNEL_USERNAME, message.from_user.id) if member.status in ['left', 'kicked']: btn = InlineKeyboardMarkup().add( InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.strip('@')}") ) await message.answer("Please join our channel first to use the bot:", reply_markup=btn) raise Exception("User not joined channel") except: btn = InlineKeyboardMarkup().add( InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.strip('@')}") ) await message.answer("Join our channel to continue:", reply_markup=btn) raise

dp.middleware.setup(ForceJoinMiddleware())

--- Start Command ---

@dp.message_handler(CommandStart()) async def start_handler(message: types.Message): name = message.from_user.first_name keyboard = InlineKeyboardMarkup() keyboard.add(InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.strip('@')}") ) keyboard.add(InlineKeyboardButton("👤 Owner", url=f"https://t.me/{(await bot.get_chat(OWNER_ID)).username}"))

await message.answer(f"Hello {name}, welcome to **raazxBot**!", reply_markup=keyboard, parse_mode="Markdown")

await bot.send_message(
    OWNER_ID,
    f"New user started bot:

Name: {message.from_user.full_name} Username: @{message.from_user.username} User ID: {message.from_user.id}" )

--- Group Join Welcome ---

@dp.chat_member_handler() async def welcome_new_member(update: types.ChatMemberUpdated): if update.new_chat_member.user.is_bot: return

if update.old_chat_member.status == 'left' and update.new_chat_member.status == 'member':
    name = update.new_chat_member.user.first_name
    user_id = update.new_chat_member.user.id

    image_url = await get_random_pinterest_image()
    welcome_msg = f"Welcome, [{name}](tg://user?id={user_id})!"

    await bot.send_photo(update.chat.id, image_url, caption=welcome_msg, parse_mode='Markdown')

--- Pinterest Image Fetch ---

async def get_random_pinterest_image(): try: async with aiohttp.ClientSession() as session: async with session.get("https://source.unsplash.com/random/600x400/?nature,tech") as resp: return str(resp.url) except: return "https://source.unsplash.com/random/600x400"

--- Run Bot ---

if name == 'main': executor.start_polling(dp, skip_updates=True)

