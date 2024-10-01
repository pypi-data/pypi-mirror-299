from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from polymorphic.admin import PolymorphicChildModelAdmin

from sage_qrcode.models import (
    MediaUrl,
    TikTokQRCode,
    FacebookQRCode,
    InstagramQRCode,
    LinkedInQRCode,
    SkypeQRCode,
    SnapchatQRCode,
    XQRCode,
    TelegramQRCode,
)
from sage_qrcode.forms import TikTokForm, MediaUrlForm, XForm
from sage_qrcode.admin.base import QRCodeParentAdmin


@admin.register(SkypeQRCode)
class SkypeQRCodeAdmin(PolymorphicChildModelAdmin, QRCodeParentAdmin):
    base_model = SkypeQRCode
    form = TikTokForm
    show_in_index = True
    list_display = ("url",)
    list_filter = ("url",)
    search_fields = ("url",)

    fieldsets = (
        (None, {"fields": ("url",)}),
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


@admin.register(TikTokQRCode)
class TikTokQRCodeAdmin(PolymorphicChildModelAdmin, QRCodeParentAdmin):
    base_model = TikTokQRCode
    form = TikTokForm
    show_in_index = True
    list_display = ("url",)
    list_filter = ("url",)
    search_fields = ("url",)

    fieldsets = (
        (None, {"fields": ("url",)}),
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


@admin.register(SnapchatQRCode)
class SnapchatQRCodeAdmin(PolymorphicChildModelAdmin, QRCodeParentAdmin):
    base_model = SnapchatQRCode
    form = TikTokForm
    list_display = ("url",)
    list_filter = ("url",)
    search_fields = ("url",)

    fieldsets = (
        (None, {"fields": ("url",)}),
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


@admin.register(XQRCode)
class XQRCodeAdmin(PolymorphicChildModelAdmin, QRCodeParentAdmin):
    base_model = XQRCode
    form = XForm
    list_display = ("url",)
    list_filter = ("url",)
    search_fields = ("url",)

    fieldsets = (
        (None, {"fields": ("url",)}),
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


@admin.register(LinkedInQRCode)
class LinkedInQRCodeAdmin(PolymorphicChildModelAdmin, QRCodeParentAdmin):
    base_model = LinkedInQRCode
    show_in_index = True
    list_display = ("url",)
    list_filter = ("url",)
    search_fields = ("url",)

    fieldsets = (
        (None, {"fields": ("url",)}),
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


@admin.register(FacebookQRCode)
class FacebookQRCodeAdmin(PolymorphicChildModelAdmin, QRCodeParentAdmin):
    base_model = FacebookQRCode
    list_display = ("url",)
    list_filter = ("url",)
    search_fields = ("url",)

    fieldsets = (
        (None, {"fields": ("url",)}),
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


@admin.register(TelegramQRCode)
class TelegramQRCodeAdmin(PolymorphicChildModelAdmin, QRCodeParentAdmin):
    base_model = TelegramQRCode
    form = TikTokForm
    list_display = ("url",)
    list_filter = ("url",)
    search_fields = ("url",)

    fieldsets = (
        (None, {"fields": ("url",)}),
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


@admin.register(InstagramQRCode)
class InstagramQRCodeAdmin(PolymorphicChildModelAdmin, QRCodeParentAdmin):
    base_model = InstagramQRCode
    form = TikTokForm
    list_display = ("url",)
    list_filter = ("url",)
    search_fields = ("url",)

    fieldsets = (
        (None, {"fields": ("url",)}),
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


@admin.register(MediaUrl)
class MediaUrlAdmin(PolymorphicChildModelAdmin, QRCodeParentAdmin):
    base_model = MediaUrl
    form = MediaUrlForm
    show_in_index = True
    list_display = ("url", "custom_gif")
    list_filter = ("url",)
    search_fields = ("url",)

    fieldsets = (
        (None, {"fields": ("url",)}),
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
