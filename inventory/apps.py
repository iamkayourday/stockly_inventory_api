from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'

    # Import signals to ensure they are registered
    def ready(self):
        import inventory.signals
