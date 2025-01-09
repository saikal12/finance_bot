from datetime import datetime, timedelta
from django.utils import timezone
from telegram_bot.models import Receipt
from django.db.models import Sum
from telegram import Update
from telegram.ext import CallbackContext
from asgiref.sync import sync_to_async
async def get_chek_summary(update: Update, context: CallbackContext):
    """Обрабатываем выбор фильтрации."""
    query = update.callback_query
    await query.answer()
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
        #total = await sync_to_async(queryset.aggregate)(total=Sum('amount'))['total']
        #total_amount = total if total else 0
        if queryset:
            receipts_text = "\n".join([
                f"Сумма: {receipt.amount}, Дата: {receipt.date_upload}, "
                f"Тип операции: {receipt.transaction_type}" for receipt in queryset
            ])

        else:
            receipts_text = "Нет чеков за указанный период."
        # Отправляем результат
        await query.edit_message_text(
                f"Чеки \n {receipts_text}\n\nОбщая сумма: {0}" #total_amount:.2f
                )
    else:
        await query.edit_message_text("Invalid filter type or no data available.")