import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

# Bot tokeni to'g'ri o'zgaruvchiga berildi
BOT_TOKEN = "8782883090:AAFJN2T7vx6SoLprymNuosKtzybR9D4I720"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Ketma-ketlik holatlarini belgilash (FSM)
class UserRegistration(StatesGroup):
    name = State()
    age = State()
    hobby = State()

# /start komandasi yuborilganda
@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await message.answer(
        f"Vaalaykum assalom, {message.from_user.first_name}! 😊\n"
        "Siz bilan tanishib olsak bo'ladimi?\n\n"
        "Ismingiz nima?"
    )
    await state.set_state(UserRegistration.name)

# Ismni qabul qilish va yoshni so'rash
@dp.message(UserRegistration.name)
async def process_name(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Iltimos, ismingizni matn ko'rinishida yozing:")
        return
        
    await state.update_data(name=message.text)
    await message.answer(f"Tanishganimdan xursandman, {message.text}! Yoshingiz nechida?")
    await state.set_state(UserRegistration.age)

# Yoshni qabul qilish va qiziqishni so'rash
@dp.message(UserRegistration.age)
async def process_age(message: Message, state: FSMContext):
    if not message.text or not message.text.isdigit():
        await message.answer("Iltimos, yoshingizni faqat raqamlarda kiriting (masalan: 18):")
        return
    
    await state.update_data(age=message.text)
    await message.answer("Ajoyib! Bo'sh vaqtlaringizda nimaga qiziqasiz? (Hobbingiz nima?):")
    await state.set_state(UserRegistration.hobby)

# Qiziqishni qabul qilish va natijani chiqarish
@dp.message(UserRegistration.hobby)
async def process_hobby(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Iltimos, qiziqishingizni matn ko'rinishida yozing:")
        return

    await state.update_data(hobby=message.text)
    user_data = await state.get_data()
    
    response = (
        "✅ <b>Ma'lumotlaringiz saqlandi!</b>\n\n"
        f"• <b>Ismingiz:</b> {user_data['name']}\n"
        f"• <b>Yoshingiz:</b> {user_data['age']} da\n"
        f"• <b>Qiziqishingiz:</b> {user_data['hobby']}\n\n"
        "Tanishganimdan juda xursandman! 🎉"
    )
    
    # Xatolik chiqmasligi uchun HTML formatidan foydalanildi
    await message.answer(response, parse_mode="HTML")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
