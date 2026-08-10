import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# Telegram token server muhitidan olinadi
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Suhbat bosqichlarini belgilash (FSM)
class UserDialog(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_hobby = State()

# 1-bosqich: /start bosilganda salomlashish va ismini so'rash
@dp.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    await message.answer("Salom! Alik olaman, hush kelibsiz! 😊\nIsmingiz nima?")
    await state.set_state(UserDialog.waiting_for_name)

# 2-bosqich: Ismni qabul qilib, yoshni so'rash
@dp.message(UserDialog.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await message.answer(f"Tanishganimdan xursandman, {message.text}! Yoshiz nechida?")
    await state.set_state(UserDialog.waiting_for_age)

# 3-bosqich: Yoshni qabul qilib, qiziqishini so'rash
@dp.message(UserDialog.waiting_for_age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(user_age=message.text)
    await message.answer("Ajoyib! Qiziqishlaringiz yoki xobbingiz nima?")
    await state.set_state(UserDialog.waiting_for_hobby)

# 4-bosqich: Qiziqishni qabul qilib, suhbatni yakunlash
@dp.message(UserDialog.waiting_for_hobby)
async def process_hobby(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data.get("user_name")
    
    await message.answer(
        f"Ma'lumotlar uchun rahmat, {name}! 🤝\n"
        f"Siz bilan suhbatlashish juda yoqimli bo'ldi. Yaxshi dam oling!"
    )
    # Suhbat holatini tozalash
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
