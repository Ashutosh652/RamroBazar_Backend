from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ramrobazar.account'

    def ready(self):
        import ramrobazar.account.signals
