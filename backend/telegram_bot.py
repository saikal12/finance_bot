import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram_bot.service.handlers.call_query_main import callback_query_handler
from backend.settings import BOT_TOKEN

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from telegram_bot.language.handler.language_handlers import choose_lang
from telegram_bot.receipt.handlers.filters import filter_receipt
from telegram_bot.receipt.handlers.receipt import handle_img
from telegram_bot.service.mini_command.start_command import start
from telegram_bot.service.mini_command.help_command import help_command
from telegram_bot.language.language_dict import translations
from telegram_bot.language.service.get_translation import get_translation
def main():
    lang_translations = translations['en']
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.PHOTO, handle_img))
    application.add_handler(CommandHandler(lang_translations['start_command'], start))
    application.add_handler(CommandHandler(lang_translations["filter_receipt_command"], filter_receipt))
    application.add_handler(CommandHandler(lang_translations["choose_language_command"], choose_lang))
    application.add_handler(MessageHandler(filters.Regex(lang_translations["choose_language_command"]), choose_lang)) #for ru not work
    application.add_handler(MessageHandler(filters.Regex(lang_translations["help_text"]), help_command))
    application.add_handler(MessageHandler(filters.Regex(lang_translations["filter_checks_command"]), filter_receipt))
    application.add_handler(CallbackQueryHandler(callback_query_handler))
    application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())