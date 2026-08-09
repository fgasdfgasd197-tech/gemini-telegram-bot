import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Logging (xatoliklarni ko'rib borish uchun)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Muloqot bosqichlari uchun konstantalar
NAME, AGE, INTERESTS, MOOD, WORK = range(5)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Botni boshlash va ismni so'rash"""
    await update.message.reply_text(
        "Salom, men Jasur AI'man! Ismingiz nima?"
    )
    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ismni saqlash va yoshni so'rash"""
    user_name = update.message.text
    context.user_data["name"] = user_name

    await update.message.reply_text(
        f"Salom, {user_name}! Yoshingiz nechida?"
    )
    return AGE


async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Yoshni saqlash va qiziqishlarni so'rash"""
    context.user_data["age"] = update.message.text

    await update.message.reply_text(
        "Qiziqishlaringiz qanday?"
    )
    return INTERESTS


async def get_interests(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Qiziqishlarni saqlash va kayfiyatni so'rash"""
    context.user_data["interests"] = update.message.text

    await update.message.reply_text(
        "Juda zo'r qiziqish! Xo'p, kayfiyatingiz qanday?"
    )
    return MOOD


async def get_mood(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Kayfiyatni saqlash va ish/faoliyatni so'rash"""
    context.user_data["mood"] = update.message.text

    await update.message.reply_text(
        "Nima ishlar bilan shug'ullanasiz?"
    )
    return WORK


async def get_work(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Oxirgi javobni olish va muloqotni yakunlash"""
    context.user_data["work"] = update.message.text
    name = context.user_data.get("name", "Do'stim")

    await update.message.reply_text(
        f"Yaxshidami, oling! Rahmat, {name}, barcha ma'lumotlar uchun."
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Muloqotni bekor qilish"""
    await update.message.reply_text("Suhbat to'xtatildi.")
    return ConversationHandler.END


def main():
    # BotFather'dan olingan TOKEN'ni shu yerga qo'ying
    TOKEN = "BOT_TOKENINGIZNI_SHU_YERGA_YOZING"

    application = ApplicationBuilder().token(TOKEN).build()

    # Muloqot konspektori (ConversationHandler)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            INTERESTS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_interests)
            ],
            MOOD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_mood)],
            WORK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_work)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    print("Bot ishga tushdi...")
    application.run_polling()


if name == "main":
    main()
