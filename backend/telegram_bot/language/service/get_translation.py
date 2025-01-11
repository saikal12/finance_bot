from telegram.ext import CallbackContext
from telegram import Update
from telegram_bot.language.language_set.UserLanguage import SetLanguage
from telegram_bot.language.service.get_user import create_user_account
from telegram_bot.language.language_dict import translations


async def get_translation(update: Update, context: CallbackContext):
    # gets the telegram user.
    # It gets the user object UserAccount
    # and sets it for the class SetLanguage

    user = update.effective_user
    user, created = await create_user_account(user)
    lang = SetLanguage(user)
    # set dict lang by user language, default en
    translation = translations.get( await lang.get_user_language(), translations['en'])
    return translation
