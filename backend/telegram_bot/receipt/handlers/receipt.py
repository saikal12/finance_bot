import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from backend.settings import API_KEY, ORG_ID
from telegram import Update
from telegram.ext import CallbackContext
from telegram_bot.receipt.analyze_save.receipt_analyzer import ReceiptAnalyzer
from telegram_bot.receipt.analyze_save.receipt_save import ReceiptSaver
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
from telegram_bot.language.service.get_user import create_user_account



async def handle_img(update: Update, context: CallbackContext):
    """ take image and"""
    from_user = update.message.from_user
    user_account, created = await create_user_account(from_user)  # get object of UserAccount
    img_file = await update.message.photo[-1].get_file()  # Receive the file
    img_bytes = await img_file.download_as_bytearray()  # download it as bytes
    try:
        analyser_object = ReceiptAnalyzer(API_KEY, ORG_ID)
        analyser_result = analyser_object.analyze_image(img_bytes)
        #analyser_result = analyser_object.plug(img_bytes)
        await update.message.reply_text(analyser_result)
        saver_object = ReceiptSaver(user_account)  # get object of UserAccount
        await saver_object.save_receipt(analyser_result)
        await update.message.reply_text("Чек обработан и сохранен.")
    except Exception as e:
        raise e
        print(f"Error: {str(e)}")