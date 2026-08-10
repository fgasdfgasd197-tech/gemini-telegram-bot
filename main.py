import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Telegram token server muhitidan olinadi
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Suhbat bosqichlarini belgilash (FSM)
class UserDialog(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_hobby = State()

# Qayta boshlash tugmasi
restart_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🔄 Qayta boshlash")]],
    resize_keyboard=True
)

# 1-bosqich: /start yoki "Qayta boshlash" tugmasi bosilganda
@dp.message(CommandStart())
@dp.message(F.text == "🔄 Qayta boshlash")
async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Salom! Man Jasur AI man, sizga qanday yordam berolaman? 😊\n\n"
        "Keling, tanishib olamiz. **Ismingiz nima?**",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="Markdown"
    )
    await state.set_state(UserDialog.waiting_for_name)

# Jarayonni bekor qilish komandasi
@dp.message(Command("cancel"))
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(
        "Suhbat bekor qilindi. Qaytadan boshlash uchun /start bosing.", 
        reply_markup=ReplyKeyboardRemove()
    )

# 2-bosqich: Ismni qabul qilish va yoshni so'rash
@dp.message(UserDialog.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if len(name) < 2:
        await message.answer("Iltimos, ismingizni to'g'ri kiriting (kamida 2 ta harf):")
        return
    
    await state.update_data(user_name=name)
    await message.answer(f"Tanishganimdan xursandman, **{name}**! 😃\nYoshingiz nechida?", parse_mode="Markdown")
    await state.set_state(UserDialog.waiting_for_age)

# 3-bosqich: Yoshni qabul qilish va xobbi so'rash (Validation bilan)
@dp.message(UserDialog.waiting_for_age)
async def process_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or not (5 <= int(message.text) <= 100):
        await message.answer("⚠️ Iltimos, yoshingizni faqat raqamlarda kiriting (masalan: 22):")
        return

    await state.update_data(user_age=message.text)
    await message.answer("Ajoyib! Qiziqishlaringiz yoki xobbingiz nima?")
    await state.set_state(UserDialog.waiting_for_hobby)

# 4-bosqich: Xobbini qabul qilish va natijani chiqarish
@dp.message(UserDialog.waiting_for_hobby)
async def process_hobby(message: types.Message, state: FSMContext):
    await state.update_data(user_hobby=message.text)
    user_data = await state.get_data()
    
    summary_text = (
        "✅ **Siz kiritgan ma'lumotlar:**\n\n"
        f"👤 **Ism:** {user_data.get('user_name')}\n"
        f"🎂 **Yosh:** {user_data.get('user_age')} yosh\n"
        f"🎯 **Xobbi:** {user_data.get('user_hobby')}\n\n"
        "Ma'lumotlar uchun rahmat! Siz bilan suhbatlashish juda yoqimli bo'ldi. ✨"
    )
    
    await message.answer(summary_text, reply_markup=restart_keyboard, parse_mode="Markdown")
    await state.clear()

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
