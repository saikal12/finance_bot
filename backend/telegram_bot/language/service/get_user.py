from telegram_bot.models import UserAccount
from asgiref.sync import sync_to_async

@sync_to_async
def create_user_account(user):
    """
    Gets the object and a boolean value whether the user has been created.
    Create the user if can`t get.
    Return user object and bool """
    # returns user object using user chat id
    user_account, created = UserAccount.objects.get_or_create(
        telegram_id=user.id,
        defaults={
            "username": user.username,
        }
    )
    return user_account, created