from telegram import Update
from telegram.ext import CallbackContext
from telegram_bot.receipt.handlers.filters import handle_filter
from telegram_bot.language.handler.language_handlers import handle_language


async def callback_query_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    callback_data = query.data

    if callback_data.startswith('language'):
        await handle_language(query, callback_data)
    elif callback_data.startswith('filter_'):
        await handle_filter(query, callback_data)
    else:
        await query.edit_message_text("Unknown action.")

