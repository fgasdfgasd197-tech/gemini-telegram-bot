import os
import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Server muhitidan olinadigan parametrlar
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # O'zingizning Telegram ID'ingizni kiriting

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ==================== DATABASE (SQLite) ====================
def init_db():
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            age TEXT,
            hobby TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_user(user_id, name, age, hobby):
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO users (user_id, name, age, hobby)
        VALUES (?, ?, ?, ?)
    """, (user_id, name, age, hobby))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, age, hobby FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_all_users():
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    conn.close()
    return [u[0] for u in users]

# ==================== STATES (FSM) ====================
class UserDialog(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_hobby = State()

class AdminStates(StatesGroup):
    waiting_for_broadcast = State()

# ==================== KEYBOARDS ====================
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 Profilim"), KeyboardButton(text="🔄 Qayta ro'yxatdan o'tish")]
    ],
    resize_keyboard=True
)

admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Statistika"), KeyboardButton(text="📢 Xabar yuborish")],
        [KeyboardButton(text="🏠 Bosh menyu")]
    ],
    resize_keyboard=True
)

# ==================== HANDLERS ====================

# 1-bosqich: /start
@dp.message(CommandStart())
@dp.message(F.text == "🔄 Qayta ro'yxatdan o'tish")
async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Salom! Man Jasur AI man, sizga qanday yordam berolaman? 😊\n\n"
        "Keling, tanishib olamiz. **Ismingiz nima?**",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="Markdown"
    )
    await state.set_state(UserDialog.waiting_for_name)

# Bekor qilish
@dp.message(Command("cancel"))
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Amal bekor qilindi.", 
        reply_markup=main_keyboard
    )

# 2-bosqich: Ism
@dp.message(UserDialog.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if len(name) < 2:
        await message.answer("Iltimos, ismingizni to'g'ri kiriting (kamida 2 ta harf):")
        return
    
    await state.update_data(user_name=name)
    await message.answer(f"Tanishganimdan xursandman, **{name}**! 😃\nYoshingiz nechida?", parse_mode="Markdown")
    await state.set_state(UserDialog.waiting_for_age)

# 3-bosqich: Yosh
@dp.message(UserDialog.waiting_for_age)
async def process_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or not (5 <= int(message.text) <= 100):
        await message.answer("⚠️ Iltimos, yoshingizni faqat raqamlarda kiriting (masalan: 22):")
        return

    await state.update_data(user_age=message.text)
    await message.answer("Ajoyib! Qiziqishlaringiz yoki xobbingiz nima?")
    await state.set_state(UserDialog.waiting_for_hobby)

# 4-bosqich: Xobbi va Bazaga saqlash
@dp.message(UserDialog.waiting_for_hobby)
async def process_hobby(message: types.Message, state: FSMContext):
    await state.update_data(user_hobby=message.text)
    user_data = await state.get_data()
    
    name = user_data.get("user_name")
    age = user_data.get("user_age")
    hobby = user_data.get("user_hobby")
    
    # Bazaga yozish
    save_user(message.from_user.id, name, age, hobby)
    
    summary_text = (
        "✅ **Siz kiritgan ma'lumotlar saqlandi:**\n\n"
        f"👤 **Ism:** {name}\n"
        f"🎂 **Yosh:** {age} yosh\n"
        f"🎯 **Xobbi:** {hobby}\n\n"
        "Rahmat! Siz bilan suhbatlashish juda yoqimli bo'ldi. ✨"
    )
    
    await message.answer(summary_text, reply_markup=main_keyboard, parse_mode="Markdown")
    await state.clear()

# Profilni ko'rish
@dp.message(F.text == "👤 Profilim")
async def show_profile(message: types.Message):
    user = get_user(message.from_user.id)
    if user:
        await message.answer(
            f"📋 **Sizning profilingiz:**\n\n"
            f"👤 **Ism:** {user[0]}\n"
            f"🎂 **Yosh:** {user[1]}\n"
            f"🎯 **Xobbi:** {user[2]}",
            parse_mode="Markdown"
        )
    else:
        await message.answer("Siz hali ro'yxatdan o'tmabsiz. /start buyrug'ini bosing.")

# Bosh menyuga qaytish
@dp.message(F.text == "🏠 Bosh menyu")
async def back_to_main(message: types.Message):
    await message.answer("Bosh menyu:", reply_markup=main_keyboard)

# ==================== ADMIN PANEL ====================
@dp.message(Command("admin"))
async def admin_cmd(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Xush kelibsiz, Admin!", reply_markup=admin_keyboard)
    else:
        await message.answer("Siz admin emassiz!")

@dp.message(F.text == "📊 Statistika")
async def show_stats(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        users = get_all_users()
        await message.answer(f"👥 Botdan foydalanuvchilar soni: **{len(users)}** ta", parse_mode="Markdown")

@dp.message(F.text == "📢 Xabar yuborish")
async def ask_broadcast_message(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni kiriting:")
        await state.set_state(AdminStates.waiting_for_broadcast)

@dp.message(AdminStates.waiting_for_broadcast)
async def send_broadcast(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        users = get_all_users()
        count = 0
        for user_id in users:
            try:
                await bot.send_message(user_id, message.text)
                count += 1
                await asyncio.sleep(0.05)
            except Exception:
                pass
        await message.answer(f"✅ Xabar **{count}** ta foydalanuvchiga muvaffaqiyatli yuborildi!", reply_markup=admin_keyboard, parse_mode="Markdown")
        await state.clear()

# ==================== MAIN RUN ====================
async def main():
    init_db()  # Bazani yaratish
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
from countryinfo import CountryInfo
import json

country_data = []

while True:
    country_name = input("Davlat nomini kiriting: ")
    if country_name == "stop":
        print("Dasturni to'htatingiz !")
        with open("information.txt", mode='a', encoding='utf-8') as file:
            json.dump(country_data, file, indent=4, ensure_ascii=False)
            break

    try:
        get_country = CountryInfo(country_name)
        data = get_country.info()

        name = data['name']
        area = data['area']
        borders = data['borders']
        capital = data['capital']
        currencies = data['currencies']
        region = data['region']
        languages = data['languages']
        timezones = data['timezones']
        population = data['population']

        print(f"{name} davlati haqida ma'lumot: \n"
              f"{name} davlati {region} qitasida joylashgan\n"
              f"{name} davlati {area} huquduga teng\n"
              f"chegaralari {borders} lar bilan chegaradosh\n"
              f"{name} davlatingin poytaxti {capital} hisoblanadi va\n"
              f"pul birligi esa {currencies}\n"
              f"qabul qilingan tillari {languages}\n"
              f"vaqt birligi esa {timezones}\n"
              f"{name} davlat aholisi {population} ga teng.\n\n")

        country_data.append({
            'name': name,
            'region': region,
            'area': area,
            'borders': borders,
            'capital': capital,
            'currencies': currencies,
            'languages': languages,
            'timezones': timezones,
            'population': population,
        })

    except:
        print("Siz davlat nomini notog'ri kiritiz manmcha !")
