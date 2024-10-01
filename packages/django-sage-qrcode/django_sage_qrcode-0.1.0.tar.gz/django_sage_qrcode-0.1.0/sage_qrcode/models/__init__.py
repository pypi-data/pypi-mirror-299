from .card import VCardQRCode
from .qrcode import QRCode
from .social_media import (
    WhatsAppQRCode,
    SkypeQRCode,
    SnapchatQRCode,
    TelegramQRCode,
    FacebookQRCode,
    XQRCode,
    InstagramQRCode,
    LinkedInQRCode,
    MediaUrl,
    TikTokQRCode,
)
from .wifi import WifiQRCode
from .epc import EPCQRCode
from .bitcoin import BitcoinQRCode
from .barcode import Barcode, BarcodeUrl, BarcodeText

__all__ = [
    "VCardQRCode",
    "QRCode",
    "WhatsAppQRCode",
    "SkypeQRCode",
    "SnapchatQRCode",
    "TelegramQRCode",
    "FacebookQRCode",
    "XQRCode",
    "InstagramQRCode",
    "LinkedInQRCode",
    "MediaUrl",
    "TikTokQRCode",
    "WifiQRCode",
    "EPCQRCode",
    "BitcoinQRCode",
    "Barcode",
    "BarcodeUrl",
    "BarcodeText",
]
