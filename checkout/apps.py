from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # ???
    name = 'checkout'

    # overriding read method, Needed because signals.py
    def ready(self):
        import checkout.signals
