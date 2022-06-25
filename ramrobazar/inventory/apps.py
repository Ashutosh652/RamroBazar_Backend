from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ramrobazar.inventory'

    def ready(self):
        import ramrobazar.inventory.signals
