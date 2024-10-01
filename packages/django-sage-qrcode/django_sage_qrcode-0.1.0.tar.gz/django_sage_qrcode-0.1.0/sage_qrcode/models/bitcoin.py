from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from sage_qrcode.models.qrcode import QRCode
from sage_qrcode.helpers.validators import validate_bitcoin_address


class BitcoinQRCode(QRCode):
    """Model representing a Bitcoin Payment QR code.

    A Bitcoin Payment QR code stores Bitcoin payment information. When
    scanned, it opens the Bitcoin wallet app with the encoded payment
    information.

    """

    bitcoin_address = models.CharField(
        max_length=34,
        validators=[validate_bitcoin_address],
        help_text=_("Bitcoin address. Example: '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'"),
        db_comment="The Bitcoin address for the payment.",
        verbose_name=_("Bitcoin Address"),
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=8,
        null=False,
        blank=False,
        validators=[MinValueValidator(0.00000001)],
        help_text=_("Amount of Bitcoin to send. Example: '0.01'"),
        db_comment="The amount of Bitcoin to send.",
        verbose_name=_("Amount"),
    )
    label = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Label for the transaction."),
        db_comment="An optional label for the transaction.",
        verbose_name=_("Label"),
    )
    message = models.TextField(
        blank=True,
        help_text=_("Message for the transaction."),
        db_comment="An optional message for the transaction.",
        verbose_name=_("Message"),
    )

    def __str__(self):
        return f"Bitcoin QR Code {self.pk} - {self.bitcoin_address}"

    def __repr__(self):
        return f"<BitcoinQRCode(id={self.pk}, bitcoin_address={self.bitcoin_address})>"

    class Meta:
        indexes = [models.Index(fields=["bitcoin_address"], name="bitcoin_address_idx")]
        ordering = ["bitcoin_address"]
        verbose_name = _("Bitcoin QR Code")
        verbose_name_plural = _("Bitcoin QR Codes")
