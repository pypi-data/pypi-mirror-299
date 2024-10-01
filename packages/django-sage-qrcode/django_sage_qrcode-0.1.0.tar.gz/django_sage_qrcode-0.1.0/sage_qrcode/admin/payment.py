from polymorphic.admin import PolymorphicChildModelAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from sage_qrcode.models import BitcoinQRCode, EPCQRCode
from sage_qrcode.forms import BitForm, EPCQRCodeForm
from sage_qrcode.admin.base import QRCodeParentAdmin


@admin.register(EPCQRCode)
class EPCQRCodeAdmin(PolymorphicChildModelAdmin, QRCodeParentAdmin):
    base_model = EPCQRCode
    form = EPCQRCodeForm
    # show_in_index = False
    list_display = ("name", "iban")
    list_filter = ("name", "amount")
    search_fields = ("name", "iban")

    fieldsets = (
        (None, {"fields": ("name", "iban", "text", "amount", "custom_gif")}),
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


@admin.register(BitcoinQRCode)
class BitcoinQRCodeAdmin(PolymorphicChildModelAdmin, QRCodeParentAdmin):
    base_model = BitcoinQRCode
    form = BitForm
    list_display = ("bitcoin_address", "amount", "label", "message")
    list_filter = ("bitcoin_address",)
    search_fields = ("bitcoin_address", "label", "message")

    fieldsets = (
        (None, {"fields": ("bitcoin_address", "amount", "label", "message")}),
        (
            _("Advanced options"),
            {
                "classes": ("collapse",),
                "fields": (
                    "size",
                    "color",
                    "second_color",
                    "third_color",
                ),
            },
        ),
    )

    def has_module_permission(self, request):
        return False
