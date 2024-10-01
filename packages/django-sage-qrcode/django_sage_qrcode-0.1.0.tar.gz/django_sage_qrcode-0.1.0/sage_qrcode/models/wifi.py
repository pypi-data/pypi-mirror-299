from django.db import models
from django.utils.translation import gettext_lazy as _
from sage_qrcode.models.qrcode import QRCode


class WifiQRCode(QRCode):
    """Model representing a WiFi QR code.

    A WiFi QR code stores the credentials for a WiFi network. When
    scanned, it allows the user to quickly connect to the WiFi network.

    """

    ssid = models.CharField(
        max_length=255,
        help_text=_("SSID of the WiFi network."),
        db_comment="The SSID of the WiFi network.",
        verbose_name=_("SSID"),
    )
    password = models.CharField(
        max_length=255,
        help_text=_("Password of the WiFi network."),
        db_comment="The password for the WiFi network.",
        verbose_name=_("WiFi Password"),
    )
    security = models.CharField(
        max_length=50,
        default="WPA",
        help_text=_("Security type of the WiFi network."),
        db_comment="The security type for the WiFi network (e.g., WPA, WPA2).",
        verbose_name=_("Security Type"),
    )

    def __str__(self):
        return f"WiFi QR Code {self.pk} for SSID {self.ssid}"

    def __repr__(self):
        return f"<WifiQRCode(id={self.pk}, ssid={self.ssid})>"

    class Meta:
        indexes = [models.Index(fields=["ssid"], name="wifi_ssid_idx")]
        ordering = ["ssid"]
        verbose_name = _("WiFi QR Code")
        verbose_name_plural = _("WiFi QR Codes")
