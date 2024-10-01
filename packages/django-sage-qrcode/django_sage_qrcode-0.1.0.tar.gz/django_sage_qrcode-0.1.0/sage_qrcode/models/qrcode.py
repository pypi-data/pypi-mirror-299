from django.db import models
from django.utils.translation import gettext_lazy as _

from colorfield.fields import ColorField
from polymorphic.models import PolymorphicModel

from sage_qrcode.mixins import TimestampMixin
from sage_qrcode.helpers.validators import validate_image_file, validate_size


class QRCode(PolymorphicModel, TimestampMixin):
    """Abstract base class for all QR code types."""

    qr_code_image = models.ImageField(
        upload_to="qr_codes/",
        blank=True,
        null=True,
        validators=[validate_image_file],
        help_text=_("The generated QR code image."),
        db_comment="The image file of the generated QR code.",
    )
    custom_gif = models.ImageField(
        upload_to="custom_gifs/",
        blank=True,
        null=True,
        validators=[validate_image_file],
        help_text=_("Custom GIF to be embedded in the QR code."),
        db_comment="An optional custom GIF that can be embedded in the QR code.",
    )
    title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Title of the QR code."),
        db_comment="A descriptive title for the QR code.",
    )
    size = models.PositiveSmallIntegerField(
        validators=[validate_size],
        help_text=_("Size of the QR code image."),
        null=True,
        blank=True,
        db_comment="The size (dimensions) of the QR code image.",
    )
    color = ColorField(
        format="hex",
        help_text=_("Color of the QR code."),
        null=True,
        blank=True,
        db_comment="The color of the QR code in hexadecimal format.",
    )
    second_color = ColorField(
        format="hex",
        help_text=_("Second color of the QR code."),
        null=True,
        blank=True,
        db_comment="The second color of the QR code in hexadecimal format.",
    )

    third_color = ColorField(
        format="hex",
        help_text=_("Third color of the QR code."),
        null=True,
        blank=True,
        db_comment="The third color of the BAR code in hexadecimal format.",
    )

    class Meta:
        verbose_name = _("QR Code")
        verbose_name_plural = _("QR Codes")

    def __str__(self):
        return f"{self.__class__.__name__} {self.pk} - {self.title or 'No Title'}"

    def __repr__(self):
        return f"<QRCode(id={self.pk}, title={self.title or 'No Title'})>"
