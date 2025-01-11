from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram import Update
from telegram_bot.language.service.get_translation import get_translation
from telegram_bot.language.language_set.UserLanguage import SetLanguage
from telegram_bot.language.service.get_user import create_user_account

async def choose_lang(update:Update , context: CallbackContext):
    translation = await get_translation(update, context)

    keyboard = [
        [InlineKeyboardButton(translation['language_ru'], callback_data="language_ru")],
        [InlineKeyboardButton(translation['language_en'], callback_data="language_en")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(translation["choose_language"], reply_markup=reply_markup)


async def handle_language(query, callback_data):
    user = query.from_user
    lang = callback_data.split('_')[1]
    user_object, b = await create_user_account(user)
    lang_object = SetLanguage(user_object)
    await lang_object.set_user_language(lang)
    await query.edit_message_text(f"Language set to {lang}.")