import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
import asyncio
from asgiref.sync import sync_to_async
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters, CallbackQueryHandler
from telegram_bot.service.filter import get_chek_summary
from backend.settings import BOT_TOKEN, API_KEY, ORG_ID
from telegram_bot.models import UserAccount, Receipt
from telegram_bot.service.ReceiptAnalyzer import ReceiptAnalyzer, ReceiptSaver
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


@sync_to_async
def create_user_account(user):
    user_account, created = UserAccount.objects.get_or_create(
        telegram_id=user.id,
        defaults={
            "username": user.username,
        }
    )
    return user_account, created


async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    user, created = await create_user_account(user)
    keyboard = [
        [KeyboardButton("Фильтровать чеки")],  # Кнопка для фильтрации чеков
        [KeyboardButton("Помощь")],  # Дополнительные кнопки
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


    if created:
        await update.message.reply_text("Аккаунт создан.", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Добро пожаловать, вы уже зарегистрированы!", reply_markup=reply_markup)


async def help_command(update: Update, context: CallbackContext):
    message = (
        "🆘 **Помощь**\n\n"
        "Я бот для управления вашими финансами. Вот что я умею:\n"
        "• Получать чеки от банков и записывать в бд\n"
        "• Фильтровать чеки по времени\n"
        "• Отображать список ваших чеков\n\n"
        "Используйте кнопки меню или команды для взаимодействия со мной."
    )
    await update.message.reply_text(message)


async def handle_img(update: Update, context: CallbackContext):
    """ take image and"""
    from_user = update.message.from_user
    user_account, created = await create_user_account(from_user)
    img_file = await update.message.photo[-1].get_file()  # Receive the file
    img_bytes = await img_file.download_as_bytearray()  # download it as bytes
    try:
        analyser_object = ReceiptAnalyzer(API_KEY, ORG_ID)
        analyser_result = analyser_object.analyze_image(img_bytes)
        #analyser_result = analyser_object.plug(img_bytes)
        await update.message.reply_text(analyser_result)
        saver_object = ReceiptSaver(user_account)
        await saver_object.save_receipt(analyser_result)
        await update.message.reply_text("Чек обработан и сохранен.")
    except Exception as e:
        raise e
        print(f"Error: {str(e)}")


async def filter_receipt(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Вчера", callback_data="yesterday")],
        [InlineKeyboardButton("За последнюю неделю", callback_data="filter_week")],
        [InlineKeyboardButton("За последний месяц", callback_data="filter_month")],
        [InlineKeyboardButton("За последние 3 месяца", callback_data="filter_3month")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите временной диапазон:", reply_markup=reply_markup)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_img))
    application.add_handler(CommandHandler("filter_receipt", filter_receipt))
    application.add_handler(MessageHandler(filters.Regex("Помощь"), help_command))
    application.add_handler(MessageHandler(filters.Regex("Фильтровать чеки"), filter_receipt))
    application.add_handler(CallbackQueryHandler(get_chek_summary))
    application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())