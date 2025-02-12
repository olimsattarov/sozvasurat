import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.filters import CommandStart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # Example: -1001234567890

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

# Command to start the bot
@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer("Salom! 😊 Ushbu bot orqali ijodingiz, fikringiz yoki savollaringizni kanalga joylash mumkin.\n\nRasm yoki matn yuboring! 📩")

# Handle text messages
@dp.message()
async def handle_text(message: types.Message):
    if message.text:
        text = f"✍️ {message.text}\n\n📢 *{message.from_user.full_name}* tomonidan yuborildi."
        await bot.send_message(CHANNEL_ID, text, parse_mode="Markdown")

# Handle photos
@dp.message(lambda msg: msg.photo)
async def handle_photo(message: types.Message):
    caption = message.caption if message.caption else "📸 Surat yuklandi!"
    text = f"{caption}\n\n📢 *{message.from_user.full_name}* tomonidan yuborildi."
    await bot.send_photo(CHANNEL_ID, message.photo[-1].file_id, caption=text, parse_mode="Markdown")

# Run the bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
