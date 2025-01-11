from django.db import models
import uuid


class UserAccount(models.Model):
    telegram_id = models.BigIntegerField(unique=True)  #getting telegram user id
    username = models.CharField(max_length=150, blank=True, null=True)  #getting from telegram username
    password = models.CharField(max_length=50, default=uuid.uuid4().hex) # generating for username to be unique


class Receipt(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE) #relation for user account getting from  telegram chat id
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    text = models.JSONField(null=True)
    date_upload = models.DateTimeField()
    transaction_type =models.CharField(max_length=150, blank=True, null=True)
    image_b64 = models.TextField()


class UserLanguage(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)  #relation for user account getting from  telegram chat id
    language = models.CharField(max_length=30, default='en')