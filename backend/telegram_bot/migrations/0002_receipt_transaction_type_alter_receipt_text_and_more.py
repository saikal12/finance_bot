# Generated by Django 5.1.4 on 2025-01-08 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='transaction_type',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='text',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='password',
            field=models.CharField(default='b6e4e04f0288496ab3807831c60fc68b', max_length=50),
        ),
    ]
