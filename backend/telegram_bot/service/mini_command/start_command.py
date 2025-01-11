from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from telegram_bot.language.service.get_user import create_user_account
from telegram_bot.language.service.get_translation import get_translation


async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    user, created = await create_user_account(user)
    translation = await get_translation(update, context)
    keyboard = [
        [KeyboardButton(translation["filter checks"])],
        [KeyboardButton(translation["help"])],
        [KeyboardButton(translation["choose_language"])]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    if created:
        await update.message.reply_text(translation["account created"], reply_markup=reply_markup)
    else:
        await update.message.reply_text(translation["account registered"], reply_markup=reply_markup)

