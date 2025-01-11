from telegram import Update
from telegram.ext import CallbackContext
from telegram_bot.language.service.get_translation import get_translation


async def help_command(update: Update, context: CallbackContext):
    translation = await get_translation(update, context)
    await update.message.reply_text(translation['helps_message'])