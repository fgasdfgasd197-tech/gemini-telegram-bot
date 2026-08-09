import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from google import genai

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Asinxron klient yaratamiz
ai_client = genai.Client(api_key=GEMINI_API_KEY)

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Salom! Men Jasur AI botiman. Sizga qanday yordam bera olaman?")

@dp.message()
async def chat_with_ai(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    try:
        # Model nomi gemini-2.0-flash ga to'g'rilandi
        response = await ai_client.aio.models.generate_content(
            model='gemini-2.0-flash',
            contents=message.text,
        )
        await message.answer(response.text)
    except Exception as e:
        print(f"Xatolik: {e}")
        await message.answer("Xatolik yuz berdi. Qaytadan urinib ko'ring.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
