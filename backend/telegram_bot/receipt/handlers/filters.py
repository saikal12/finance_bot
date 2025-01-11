from datetime import datetime, timedelta
from django.utils import timezone
from telegram_bot.models import Receipt
from asgiref.sync import sync_to_async
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram_bot.language.service.get_translation import get_translation
from telegram_bot.language.language_dict import translations
async def filter_receipt(update: Update, context: CallbackContext):
    """
    Buttons to filter peceipt by period.
    Get dinamic button based on the user's language"""
    translation = await get_translation(update, context)
    keyboard = [
        [InlineKeyboardButton(translation['filter_yesterday'], callback_data="yesterday")],
        [InlineKeyboardButton(translation['filter_week'], callback_data="filter_week")],
        [InlineKeyboardButton(translation['filter_month'], callback_data="filter_month")],
        [InlineKeyboardButton(translation['filter_3month'], callback_data="filter_3month")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(translation['select time period'], reply_markup=reply_markup)


async def handle_filter(query, callback_data):
    """Processing the filter selection."""

    filter_type = query.data
    today = datetime.now()
    if filter_type == 'yesteday':
        start_date = timezone.make_aware(today - timedelta(days=1))
    elif filter_type == 'filter_week':
        start_date = timezone.make_aware(today - timedelta(days=7))
    elif filter_type == 'filter_month':
        start_date = timezone.make_aware(today - timedelta(days=30))
    else:
        start_date = timezone.make_aware(today - timedelta(days=90))

    if start_date:
        queryset = await sync_to_async(list)(Receipt.objects.filter(date_upload__gte=start_date))
        # total = await sync_to_async(queryset.aggregate)(total=Sum('amount'))['total']
        # total_amount = total if total else 0
        if queryset:
            receipts_text = "\n".join([
                f"Сумма: {receipt.amount}, Дата: {receipt.date_upload}, "
                f"Тип операции: {receipt.transaction_type}" for receipt in queryset
            ])

        else:
            receipts_text = "Нет чеков за указанный период."
        # Отправляем результат
        await query.edit_message_text(
            f"Чеки \n {receipts_text}\n\nОбщая сумма: {0}"  # total_amount:.2f
        )
    else:
        await query.edit_message_text("Invalid filter type or no data available.")