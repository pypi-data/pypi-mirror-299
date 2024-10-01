from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from sage_qrcode.models.qrcode import QRCode
from sage_qrcode.helpers.validators import validate_phone_number


class VCardQRCode(QRCode):
    """Model representing a VCard QR code.

    A VCard QR code stores information about an individual, such as
    their name, email, phone number, and more. When scanned, it allows
    the user to easily add the contact details to their address book.

    """

    full_name = models.CharField(
        max_length=255,
        help_text=_("Full name of the individual."),
        db_comment="The name of the individual represented in the VCard QR code.",
        verbose_name=_("Full Name"),
    )
    display_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Display name of the individual."),
        db_comment="An optional display name for the individual.",
        verbose_name=_("Display Name"),
    )
    email = models.EmailField(
        null=True,
        blank=True,
        help_text=_("Email address of the individual."),
        db_comment="The email address of the individual.",
        verbose_name=_("Email"),
    )
    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        validators=[validate_phone_number],
        help_text=_("Phone number of the individual."),
        db_comment="The phone number of the individual.",
        verbose_name=_("Phone Number"),
    )
    url = models.URLField(
        null=True,
        blank=True,
        help_text=_("URL of the individual's website or profile."),
        db_comment="The URL to the individual's website or profile.",
        verbose_name=_("Website URL"),
    )
    org = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Name of the organization."),
        db_comment="The organization name associated with the individual.",
        verbose_name=_("Organization"),
    )
    address = models.TextField(
        null=True,
        blank=True,
        help_text=_("Physical address of the individual."),
        db_comment="The physical address of the individual.",
        verbose_name=_("Address"),
    )
    phone_number = models.CharField(
        _("Phone Number"),
        max_length=14,
        null=True,
        blank=True,
        validators=[validate_phone_number],
        error_messages={
            "unique": _("This phone number already exists."),
            "validator_e164": _(
                "Please enter a valid phone number in E164 format (+9...)."
            ),
        },
        help_text=_("Phone number in E164 format."),
        db_comment="The phone number of the individual in E164 format.",
    )

    def __str__(self):
        return f"VCard QR Code {self.pk} for {self.display_name}"

    def __repr__(self):
        return f"<VCardQRCode(id={self.pk}, name={self.display_name})>"

    def clean(self):
        if not self.full_name:
            raise ValidationError(_("Name is required for VCard QR Code."))

    class Meta:
        indexes = [
            models.Index(fields=["full_name"], name="vcard_fullname_idx"),
            models.Index(fields=["email"], name="vcard_email_idx"),
        ]
        ordering = ["full_name"]
        verbose_name = _("VCard QR Code")
        verbose_name_plural = _("VCard QR Codes")
