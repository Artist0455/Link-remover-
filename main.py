from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.executor import start_webhook
import os
import re

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = os.getenv("WEBHOOK_URL") or "https://YOUR_RENDER_URL" + WEBHOOK_PATH

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

LINK_PATTERN = re.compile(r"https?://\S+|t\.me/\S+")

# Example roles in-memory (can replace with DB)
admins = set()
global_bans = set()

@dp.message_handler()
async def handle_messages(message: types.Message):
    if message.from_user.id in global_bans:
        await message.delete()
        return

    if LINK_PATTERN.search(message.text or ""):
        if message.from_user.id not in admins:
            await message.delete()
            await message.reply("Links are not allowed.")
    # Additional handlers here...

# Commands
@dp.message_handler(commands=["ban"])
async def cmd_ban(message: types.Message):
    if message.from_user.id in admins:
        if message.reply_to_message:
            user = message.reply_to_message.from_user.id
            global_bans.add(user)
            await message.reply(f"Globally banned user {user}")

@dp.message_handler(commands=["broadcast"])
async def cmd_broadcast(message: types.Message):
    if message.from_user.id in admins:
        text = message.get_args()
        chats = [message.chat.id]  # Simple; ideally track chat IDs
        for cid in chats:
            await bot.send_message(cid, text)

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
    )
  
