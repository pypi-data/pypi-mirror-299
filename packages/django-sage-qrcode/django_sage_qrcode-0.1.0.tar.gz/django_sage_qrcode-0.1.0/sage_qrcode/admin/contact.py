from polymorphic.admin import PolymorphicChildModelAdmin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from sage_qrcode.models import VCardQRCode, WifiQRCode
from sage_qrcode.forms import VCardQRCodeForm, WiFiQRCodeForm
from sage_qrcode.admin.base import QRCodeParentAdmin


@admin.register(VCardQRCode)
class VCardQRCodeAdmin(PolymorphicChildModelAdmin, QRCodeParentAdmin):
    base_model = VCardQRCode
    form = VCardQRCodeForm
    list_display = ("full_name", "display_name", "email", "phone", "url", "custom_gif")
    list_filter = ("full_name", "display_name", "email")
    search_fields = ("full_name", "display_name", "email")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "display_name",
                    "full_name",
                    "email",
                    "phone",
                    "url",
                    "custom_gif",
                )
            },
        ),
        (
            _("Advanced options"),
            {
                "classes": ("collapse",),
                "fields": ("org", "size", "color", "second_color", "third_color"),
            },
        ),
    )

    def has_module_permission(self, request):
        return False


@admin.register(WifiQRCode)
class WiFiQRCodeAdmin(QRCodeParentAdmin):
    base_model = WifiQRCode
    form = WiFiQRCodeForm
    list_display = ("ssid", "password", "security", "custom_gif")
    list_filter = ("ssid", "security")
    search_fields = ("ssid", "security")

    fieldsets = (
        (None, {_("fields"): ("ssid", "password", "security", "custom_gif")}),
        (
            _("Advanced options"),
            {
                "classes": ("collapse",),
                "fields": ("size", "color", "second_color", "third_color"),
            },
        ),
    )

    def has_module_permission(self, request):
        return False
