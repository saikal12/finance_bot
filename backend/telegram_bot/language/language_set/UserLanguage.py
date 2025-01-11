from telegram_bot.models import UserLanguage
from asgiref.sync import sync_to_async


class SetLanguage:
    def __init__(self, user_account):
        # get object of UserAccount and init
        self.user_account = user_account

    async def get_user_language(self):
        """Get user language from db.
        Sets english by default """

        try:
            # get user id by create async
            user_lang = await sync_to_async(UserLanguage.objects.get)(user=self.user_account.id)
            return user_lang.language
        except UserLanguage.DoesNotExist:
            return 'en'

    async def set_user_language(self, language):
        """
        Get UserLanguage object and save (create or update users language)
        Args:
            language: user`s sets language
        Returns:

        """
        # get or create UserLanguage object by using UserAccount object id as primary key
        user_language, created = await sync_to_async(UserLanguage.objects.get_or_create)(user_id=self.user_account.id)
        user_language.language = language
        # save users language
        await sync_to_async(user_language.save)()