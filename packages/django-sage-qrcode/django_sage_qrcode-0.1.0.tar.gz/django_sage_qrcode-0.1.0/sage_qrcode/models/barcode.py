from django.db import models
from django.utils.translation import gettext_lazy as _

from colorfield.fields import ColorField
from polymorphic.models import PolymorphicModel

from sage_qrcode.mixins import TimestampMixin
from sage_qrcode.helpers.validators import validate_image_file


class Barcode(PolymorphicModel, TimestampMixin):
    """Abstract base class for all QR code types."""

    bar_code_image = models.ImageField(
        upload_to="bar_codes/",
        blank=True,
        null=True,
        validators=[validate_image_file],
        help_text=_("The generated bar code image."),
        db_comment="The image file of the generated bar code.",
    )

    title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Title of the BAR code."),
        db_comment="A descriptive title for the BAR code.",
    )

    color = ColorField(
        format="hex",
        help_text=_("Color of the BAR code."),
        null=True,
        blank=True,
        db_comment="The color of the BAR code in hexadecimal format.",
    )
    second_color = ColorField(
        format="hex",
        help_text=_("Second color of the QR code."),
        null=True,
        blank=True,
        db_comment="The second color of the BAR code in hexadecimal format.",
    )

    class Meta:
        verbose_name = _("Bar Code")
        verbose_name_plural = _("Bar Codes")

    def __str__(self):
        return f"{self.__class__.__name__} {self.pk} - {self.title or 'No Title'}"

    def __repr__(self):
        return f"<QRCode(id={self.pk}, title={self.title or 'No Title'})>"


class BarcodeUrl(Barcode):
    """Model representing a Barcode URL QR code.

    A Barcode URL QR code stores the URL of media content such as videos
    or audio. When scanned, it directs the user to the Barcode url
    content.

    """

    url = models.URLField(
        help_text=_("URL of the barcode content."),
        db_comment="The URL of the barcode content.",
        verbose_name=_("barcode URL"),
    )

    def __str__(self):
        return f"BARCODE URL QR Code {self.pk} for {self.url}"

    def __repr__(self):
        return f"<BARCODE(id={self.pk}, url={self.url})>"

    class Meta:
        indexes = [models.Index(fields=["url"], name="barcode_url_idx")]
        ordering = ["url"]
        verbose_name = _(" URL Barcode")
        verbose_name_plural = _("URL Barcode")


class BarcodeText(Barcode):
    """Model representing a Text  bar code.

    A Text bar stores the URL of media content such as videos or audio.
    When scanned, it directs the user to the media content.

    """

    body = models.TextField(
        blank=True,
        help_text=_("Body of the barcode."),
        db_comment="The body of the barcode.",
        verbose_name=_("body"),
    )

    def __str__(self):
        return f"BARCODE body {self.pk} for {self.body}"

    def __repr__(self):
        return f"<BARCODE(id={self.pk}, url={self.body})>"

    class Meta:
        indexes = [models.Index(fields=["body"], name="body_idx")]
        ordering = ["body"]
        verbose_name = _("Barcode Text")
        verbose_name_plural = _("Barcode Texts")
