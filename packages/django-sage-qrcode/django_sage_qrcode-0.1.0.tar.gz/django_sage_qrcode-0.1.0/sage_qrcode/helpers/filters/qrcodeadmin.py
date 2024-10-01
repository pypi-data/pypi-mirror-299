from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _

from sage_qrcode.models import (
    VCardQRCode,
    WifiQRCode,
    MediaUrl,
    EPCQRCode,
)


class QRCodeTypeFilter(SimpleListFilter):
    """A custom filter for Django admin to filter QR codes by type.

    This filter allows the admin interface to display QR codes based on
    their type, such as VCard, WiFi, Social Media, Media URL, or EPC.

    """

    title = _("QR Code Type")
    parameter_name = "qr_code_type"

    def lookups(self, request, model_admin):
        """Returns a list of tuples for the filter options.

        Each tuple contains a value and a label that represents a QR code type.

        Args:
            request (HttpRequest): The current request object.
            model_admin (ModelAdmin): The model admin object.

        Returns:
            list: A list of tuples containing filter options.

        """
        return (
            ("vcard", _("VCard QR Code")),
            ("wifi", _("WiFi QR Code")),
            ("socialmedia", _("Social Media QR Code")),
            ("mediaurl", _("Media URL QR Code")),
            ("epc", _("EPC QR Code")),
        )

    def queryset(self, request, queryset):
        """Filters the queryset based on the selected QR code type.

        Args:
            request (HttpRequest): The current request object.
            queryset (QuerySet): The queryset of the model being filtered.

        Returns:
            QuerySet: The filtered queryset based on the selected QR code type.

        """
        if self.value() == "vcard":
            return queryset.instance_of(VCardQRCode)
        if self.value() == "wifi":
            return queryset.instance_of(WifiQRCode)
        if self.value() == "mediaurl":
            return queryset.instance_of(MediaUrl)
        if self.value() == "epc":
            return queryset.instance_of(EPCQRCode)
        return queryset
