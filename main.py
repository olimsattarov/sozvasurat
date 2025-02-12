import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
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

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Command to start the bot
@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer("Salom! 😊 Ushbu bot orqali ijodingiz, fikringiz yoki savollaringizni kanalga joylash mumkin.\n\nRasm yoki matn yuboring! 📩")

# Handle text messages
@dp.message(F.text)
async def handle_text(message: types.Message):
    text = f"✍️ {message.text}\n\n📢 *{message.from_user.full_name}* tomonidan yuborildi. \n Bot orqali yozing @sozvasuratbot"
    await bot.send_message(CHANNEL_ID, text, parse_mode="Markdown")
    logging.info("✅ Text sent successfully.")

# Handle photos (Fixed)
@dp.message(F.content_type == ContentType.PHOTO)
async def handle_photo(message: types.Message):
    logging.info("✅ Image received!")  # Debugging log

    caption = message.caption if message.caption else "📸 Surat yuklandi!"
    text = f"{caption}\n\n📢 *{message.from_user.full_name}* tomonidan yuborildi. \n Bot orqali yozing @sozvasuratbot"

    try:
        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=message.photo[-1].file_id,
            caption=text,
            parse_mode="Markdown"
        )
        logging.info("✅ Image sent successfully.")
    except Exception as e:
        logging.error(f"❌ Failed to send image: {e}")

# Run the bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
