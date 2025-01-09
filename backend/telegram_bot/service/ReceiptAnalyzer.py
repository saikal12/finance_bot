import json
import base64
from openai import OpenAI
from telegram_bot.models import Receipt
from asgiref.sync import sync_to_async


class ReceiptAnalyzer:
    """Analyzing receipt with ai and save data in db """

    def __init__(self, api_key, org_id=None):
        """
        Initialize the analyzer with OpenAI credentials

        Args:
            api_key (str): OpenAI API key
            org_id (str, optional): OpenAI organization ID
        """
        self.client = OpenAI(
            api_key=api_key,
            organization=org_id
        )

        self.default_prompt = """
            Analyze the image of a receipt and extract the following fields:
            1. "amount" — The total amount, as a number with two decimal places.
            2. "date_upload" — The date of the transaction in the format YYYY-MM-DD.
            3. "transaction_type" — 
            A string describing the type of transaction 
            (e.g., "paid", "incoming transfer", "outgoing transfer"). 
            Use Russian if the receipt is in Russian (например, "оплата","пополнено", "услуга", "входящий перевод").
            4. "detail text" - if there is additional information such as the recipient or source of funds
            Format your response exactly as this JSON schema:
            {
            "amount": "DecimalField(max_digits=10, decimal_places=2)", 
            "date_upload": "date YYYY-MM-DD",
            "transaction type": "string", 
            "text": dict , 
            }
            Use the Russian text from the receipt to identify these fields. If you cannot find a value, return null for that field.
            if you cannot find all field return JSON schema:
            {
            error message : reason why you cannot find all field 
            }
        """

    def plug(self, image_bytes):
        return json.dumps({
            "amount": "400.00",
            "date_upload": "2024-12-05",
            "transaction_type": "пополнено",
            "text": {
                "source": "Эл. кошелек",
                "detail": "Пополнение O!Деньги"
            },
            "image_b64": "base64 format string"
            })


    def analyze_image(self, image_bytes):
        """
        Send image to ChatGPT Vision API and get analysis

        Args:
            image_bytes (byte): image in bytes format

        Returns:
            str: JSON string containing the analysis
            {
            "amount": "DecimalField(max_digits=10, decimal_places=2)",
            "date_upload": "date YYYY-MM-DD",
            "transaction type": "string",
            "text": dict
            "image_b64": "string"
            }
        """

        try:
            b64 = self._img_encode(image_bytes)
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a receipt analyzer."},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": self.default_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{b64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )

            result = response.choices[0].message.content
            print(result)
            return result
        except Exception as e:
            return {"error_message": f"Error analyzing receipt: {str(e)}"}

    def _img_encode(self, img_bytes):
        """
        Encoding image bytes to base64 string
        Arg:
            img_bytes (bytes): Byte content of the image.
        Returns:
            str: Base64 encoded string of the image.
        """
        try:
            return base64.b64encode(img_bytes).decode('utf-8')
        except Exception as e:
            raise Exception(f"Error encoding image: {str(e)}")


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
