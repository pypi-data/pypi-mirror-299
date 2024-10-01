from django.apps import AppConfig


class QrcodeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sage_qrcode"

    def ready(self) -> None:
        import sage_qrcode.check