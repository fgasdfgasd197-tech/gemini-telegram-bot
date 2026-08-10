import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

# Bot tokenini shu yerga yozing
BOT_TOKEN = "BOT_TOKENINI_SHUYERGA_YOZING"

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
    await message.answer(f"Vaalaykum assalom, {message.from_user.first_name}! 😊\nSiz bilan tanishib olsak bo'ladimi?\n\nIsmingiz nima?")
    await state.set_state(UserRegistration.name)

# Ismni qabul qilish va yoshni so'rash
@dp.message(UserRegistration.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(f"Tanishganimdan xursandman, {message.text}!  Yoshingiz nechida?")
    await state.set_state(UserRegistration.age)

# Yoshni qabul qilish va qiziqishni so'rash
@dp.message(UserRegistration.age)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Iltimos, yoshingizni faqat raqamlarda kiriting (masalan: 18):")
        return
    
    await state.update_data(age=message.text)
    await message.answer("Ajoyib! Bo'sh vaqtlaringizda nimaga qiziqasiz? (Hobbingiz nima?):")
    await state.set_state(UserRegistration.hobby)

# Qiziqishni qabul qilish va natijani chiqarish
@dp.message(UserRegistration.hobby)
async def process_hobby(message: Message, state: FSMContext):
    await state.update_data(hobby=message.text)
    
    # Barcha yig'ilgan ma'lumotlarni olish
    user_data = await state.get_data()
    
    response = (
        " Sobiq ma'lumotlaringiz saqlandi!\n\n"
        f"• **Ismingiz:** {user_data['name']}\n"
        f"• **Yoshingiz:** {user_data['age']} da\n"
        f"• **Qiziqishingiz:** {user_data['hobby']}\n\n"
        "Tanishganimdan juda xursandman! "
    )
    
    await message.answer(response, parse_mode="Markdown")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
