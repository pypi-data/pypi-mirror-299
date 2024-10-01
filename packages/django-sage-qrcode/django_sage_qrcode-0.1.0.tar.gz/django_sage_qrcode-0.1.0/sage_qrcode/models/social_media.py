from django.db import models
from django.utils.translation import gettext_lazy as _
from sage_qrcode.models.qrcode import QRCode

from sage_qrcode.helpers.validators import (
    validate_tiktok,
    validate_snapchat,
    validate_instagram,
    validate_facebook,
    validate_telegram,
    validate_linkedin,
    validate_x,
    validate_skype,
    validate_phone_number,
)


class WhatsAppQRCode(QRCode):
    """Model representing a WhatsApp QR code.

    A WhatsApp QR code stores a phone number with an optional message.
    When scanned, it opens WhatsApp with the encoded information.

    """

    phone_number = models.CharField(
        max_length=20,
        validators=[validate_phone_number],
        help_text=_("WhatsApp phone number. Example: +1234567890"),
        db_comment="The WhatsApp phone number.",
        verbose_name=_("WhatsApp Phone Number"),
    )
    message = models.TextField(
        blank=True,
        help_text=_("Message to be sent. Example: 'Hello, this is a test message.'"),
        db_comment="The message to be sent via WhatsApp.",
        verbose_name=_("Message"),
    )

    def __str__(self):
        return f"WhatsApp QR Code {self.pk} - {self.phone_number}"

    def __repr__(self):
        return f"<WhatsAppQRCode(id={self.pk}, phone_number={self.phone_number})>"

    class Meta:
        indexes = [
            models.Index(fields=["phone_number"], name="whatsapp_phone_number_idx")
        ]
        ordering = ["phone_number"]
        verbose_name = _("WhatsApp QR Code")
        verbose_name_plural = _("WhatsApp QR Codes")


class SkypeQRCode(QRCode):
    url = models.URLField(
        help_text=_(
            "URL of the Skype profile. Example: 'https://www.skype.com/username'"
        ),
        validators=[validate_skype],
        db_comment="The URL of the Skype profile.",
        verbose_name=_("Skype URL"),
    )

    def __str__(self):
        return f"Skype QR Code {self.pk} for {self.url}"

    def __repr__(self):
        return f"<SkypeQRCode(id={self.pk}, url={self.url})>"

    class Meta:
        indexes = [models.Index(fields=["url"], name="skype_url_idx")]
        ordering = ["url"]
        verbose_name = _("Skype QR Code")
        verbose_name_plural = _("Skype QR Codes")


class TikTokQRCode(QRCode):
    """Model representing a TikTok QR code.

    A TikTok QR code stores the URL of a TikTok profile. When scanned,
    it directs the user to the TikTok profile page.

    """

    url = models.URLField(
        help_text=_(
            "URL of the TikTok profile. Example: 'https://www.tiktok.com/@username'"
        ),
        validators=[validate_tiktok],
        db_comment="The URL of the TikTok profile.",
        verbose_name=_("TikTok URL"),
    )

    def __str__(self):
        return f"TikTok QR Code {self.pk} for {self.url}"

    def __repr__(self):
        return f"<TikTokQRCode(id={self.pk}, url={self.url})>"

    class Meta:
        indexes = [models.Index(fields=["url"], name="tiktok_url_idx")]
        ordering = ["url"]
        verbose_name = _("TikTok QR Code")
        verbose_name_plural = _("TikTok QR Codes")


class SnapchatQRCode(QRCode):
    """Model representing a Snapchat QR code.

    A Snapchat QR code stores the URL of a Snapchat profile. When
    scanned, it directs the user to the Snapchat profile page.

    """

    url = models.URLField(
        help_text=_(
            "URL of the Snapchat profile. Example: 'https://www.snapchat.com/add/username'"
        ),
        validators=[validate_snapchat],
        db_comment="The URL of the Snapchat profile.",
        verbose_name=_("Snapchat URL"),
    )

    def __str__(self):
        return f"Snapchat QR Code {self.pk} for {self.url}"

    def __repr__(self):
        return f"<SnapchatQRCode(id={self.pk}, url={self.url})>"

    class Meta:
        indexes = [models.Index(fields=["url"], name="snapchat_url_idx")]
        ordering = ["url"]
        verbose_name = _("Snapchat QR Code")
        verbose_name_plural = _("Snapchat QR Codes")


class InstagramQRCode(QRCode):
    """Model representing an Instagram QR code.

    An Instagram QR code stores the URL of an Instagram profile. When
    scanned, it directs the user to the Instagram profile page.

    """

    url = models.URLField(
        help_text=_(
            "URL of the Instagram profile. Example: 'https://www.instagram.com/username'"
        ),
        validators=[validate_instagram],
        db_comment="The URL of the Instagram profile.",
        verbose_name=_("Instagram URL"),
    )

    def __str__(self):
        return f"Instagram QR Code {self.pk} for {self.url}"

    def __repr__(self):
        return f"<InstagramQRCode(id={self.pk}, url={self.url})>"

    class Meta:
        indexes = [models.Index(fields=["url"], name="instagram_url_idx")]
        ordering = ["url"]
        verbose_name = _("Instagram QR Code")
        verbose_name_plural = _("Instagram QR Codes")


class FacebookQRCode(QRCode):
    """Model representing a Facebook QR code.

    A Facebook QR code stores the URL of a Facebook profile. When
    scanned, it directs the user to the Facebook profile page.

    """

    url = models.URLField(
        help_text=_(
            "URL of the Facebook profile. Example: 'https://www.facebook.com/username'"
        ),
        validators=[validate_facebook],
        db_comment="The URL of the Facebook profile.",
        verbose_name=_("Facebook URL"),
    )

    def __str__(self):
        return f"Facebook QR Code {self.pk} for {self.url}"

    def __repr__(self):
        return f"<FacebookQRCode(id={self.pk}, url={self.url})>"

    class Meta:
        indexes = [models.Index(fields=["url"], name="facebook_url_idx")]
        ordering = ["url"]
        verbose_name = _("Facebook QR Code")
        verbose_name_plural = _("Facebook QR Codes")


class TelegramQRCode(QRCode):
    """Model representing a Telegram QR code.

    A Telegram QR code stores the URL of a Telegram profile. When
    scanned, it directs the user to the Telegram profile page.

    """

    url = models.URLField(
        help_text=_("URL of the Telegram profile. Example: 'https://t.me/username'"),
        validators=[validate_telegram],
        db_comment="The URL of the Telegram profile.",
        verbose_name=_("Telegram URL"),
    )

    def __str__(self):
        return f"Telegram QR Code {self.pk} for {self.url}"

    def __repr__(self):
        return f"<TelegramQRCode(id={self.pk}, url={self.url})>"

    class Meta:
        indexes = [models.Index(fields=["url"], name="telegram_url_idx")]
        ordering = ["url"]
        verbose_name = _("Telegram QR Code")
        verbose_name_plural = _("Telegram QR Codes")


class LinkedInQRCode(QRCode):
    """Model representing a LinkedIn QR code.

    A LinkedIn QR code stores the URL of a LinkedIn profile. When
    scanned, it directs the user to the LinkedIn profile page.

    """

    url = models.URLField(
        help_text=_(
            "URL of the LinkedIn profile. Example: 'https://www.linkedin.com/in/username'"
        ),
        validators=[validate_linkedin],
        db_comment="The URL of the LinkedIn profile.",
        verbose_name=_("LinkedIn URL"),
    )

    def __str__(self):
        return f"LinkedIn QR Code {self.pk} for {self.url}"

    def __repr__(self):
        return f"<LinkedInQRCode(id={self.pk}, url={self.url})>"

    class Meta:
        indexes = [models.Index(fields=["url"], name="linkedin_url_idx")]
        ordering = ["url"]
        verbose_name = _("LinkedIn QR Code")
        verbose_name_plural = _("LinkedIn QR Codes")


class XQRCode(QRCode):
    """Model representing a Twitter QR code.

    A X (old Twitter) QR code stores the URL of a Twitter profile. When
    scanned, it directs the user to the Twitter profile page.

    """

    url = models.URLField(
        help_text=_(
            "URL of the X profile. Example: 'https://www.twitter.com/username'"
        ),
        validators=[validate_x],
        db_comment="The URL of the Twitter profile.",
        verbose_name=_("Twitter URL"),
    )

    def __str__(self):
        return f"Twitter QR Code {self.pk} for {self.url}"

    def __repr__(self):
        return f"<TwitterQRCode(id={self.pk}, url={self.url})>"

    class Meta:
        indexes = [models.Index(fields=["url"], name="twitter_url_idx")]
        ordering = ["url"]
        verbose_name = _("Twitter QR Code")
        verbose_name_plural = _("Twitter QR Codes")


class MediaUrl(QRCode):
    """Model representing a media URL QR code.

    A media URL QR code stores the URL of media content such as videos
    or audio. When scanned, it directs the user to the media content.

    """

    url = models.URLField(
        help_text=_("URL of the media content."),
        db_comment="The URL of the media content.",
        verbose_name=_("Media URL"),
    )

    def __str__(self):
        return f"Media URL QR Code {self.pk} for {self.url}"

    def __repr__(self):
        return f"<MediaUrl(id={self.pk}, url={self.url})>"

    class Meta:
        indexes = [models.Index(fields=["url"], name="media_url_idx")]
        ordering = ["url"]
        verbose_name = _("Media URL QR Code")
        verbose_name_plural = _("Media URL QR Codes")
