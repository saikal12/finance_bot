from telegram_bot.models import Receipt
from asgiref.sync import sync_to_async
import json


class ReceiptSaver:
    """Get json response and insert in Receipt table"""
    def __init__(self, user_account):
        self.user_account = user_account

    async def save_receipt(self, json_text):
        """
        Save receipt data to the database.
        Args:
            json_text (str): Raw JSON text from AI response
        Returns:
            receipt object
        """
        try:
            # Clean the JSON text (remove markdown code blocks if present)
            if json_text.startswith('```'):
                lines = json_text.strip().split('\n')[1:-1]  # Remove first and last lines
                json_text = '\n'.join(lines)

            # Parse JSON to validate it
            data = json.loads(json_text)
            receipt = await sync_to_async(Receipt.objects.create)(
                user=self.user_account,
                amount=data.get("amount"),
                text=data.get("text"),
                date_upload=data.get("date_upload"),
                transaction_type=data.get("transaction_type")
            )
            return receipt
        except Exception as e:
            raise Exception(f"Error saving receipt: {str(e)}")