# Generated by Django 5.1.4 on 2025-01-08 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0002_receipt_transaction_type_alter_receipt_text_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraccount',
            old_name='user_id',
            new_name='telegram_id',
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='password',
            field=models.CharField(default='10de7c2c2f974d18a6b5d5b452d526df', max_length=50),
        ),
    ]
