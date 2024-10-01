from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from sage_qrcode.models import Barcode, BarcodeUrl, BarcodeText
from sage_qrcode.utils.admin import generate_barcode_image, save_barcode_image
from sage_qrcode.admin.actions import download_barcode_action


@admin.register(Barcode)
class BarcodeParentAdmin(PolymorphicParentModelAdmin):
    base_model = Barcode
    child_models = (BarcodeUrl, BarcodeText)
    list_display = ("title","get_barcode_type", "color", "second_color", "created", "modified")
    list_filter = ("created", "modified", "color", "second_color")
    search_fields = ("title",)
    actions = [download_barcode_action]

    fieldsets = (
        (None, {"fields": ("title", "color", "second_color")}),
        (
            _("Image"),
            {
                "fields": ("bar_code_image",),
            },
        ),
    )

    @admin.display(description=_("Bar Code Type"))
    def get_barcode_type(self, obj):
        return obj.get_real_instance_class()._meta.verbose_name

    def save_model(self, request, obj, form, change):
        barcode_image = generate_barcode_image(obj)
        save_barcode_image(obj, barcode_image)
        super().save_model(request, obj, form, change)


@admin.register(BarcodeUrl)
class BarcodeUrlAdmin(PolymorphicChildModelAdmin, BarcodeParentAdmin):
    base_model = BarcodeUrl
    show_in_index = True
    list_display = ("title",)
    list_filter = ("created", "modified", "url", "color", "second_color")
    search_fields = ("title", "url")

    fieldsets = (
        (None, {"fields": ("title", "url", "color", "second_color")}),
        (
            _("Image"),
            {
                "fields": ("bar_code_image",),
            },
        ),
    )

    def get_fields(self, request, obj=None):
        return ["url", "color", "second_color"]

    def has_module_permission(self, request):
        return False


@admin.register(BarcodeText)
class BarcodeTextAdmin(PolymorphicChildModelAdmin, BarcodeParentAdmin):
    base_model = BarcodeText
    show_in_index = True
    list_display = (
        "id",
        "title",
        "body",
        "color",
        "second_color",
        "created",
        "modified",
    )
    list_filter = ("created", "modified", "color", "second_color")
    search_fields = ("title", "body")

    fieldsets = (
        (None, {"fields": ("title", "body", "color", "second_color")}),
        (
            _("Image"),
            {
                "fields": ("bar_code_image",),
            },
        ),
    )

    def get_fields(self, request, obj=None):
        return ["body", "color", "second_color"]

    def has_module_permission(self, request):
        return False
