import logging
from typing import Optional
from pathlib import Path
from segno import helpers

from sage_qrcode.service.base import QRCodeBase
from sage_qrcode.utils import add_text_to_image, add_frame_to_image
from sage_qrcode.helpers.type import HexCode

logger = logging.getLogger(__name__)


class ContactQRCode(QRCodeBase):
    """A class for generating specific types of QR codes like WiFi, MeCard, and VCard."""

    def generate_wifi_qr_code(
        self,
        ssid: str,
        password: str,
        security_type: str = "WPA",
        save: bool = False,
        custom: Path = None,
        frame_type: Optional[str] = None,
        color: HexCode = "#000000",
        size: int = 10,
        color2: HexCode = "#FFFFFF",
        color3: HexCode = "#000000",
    ) -> None:
        """Generates a QR code for connecting to a WiFi network."""
        logger.debug("Generating WiFi QR code for SSID: %s", ssid)
        wifi_data = helpers.make_wifi_data(
            ssid=ssid, password=password, security=security_type
        )
        result = self.generate_qr_code(
            data=wifi_data, custom=custom, color=color, scale=size
        )
        if frame_type:
            logger.info("Adding frame_type to QR code.")
            self.qr_image = add_frame_to_image(self.qr_image, frame_type)
        if not result:
            logger.info("Adding text to QR code image.")
            self.qr_image = add_text_to_image(self.qr_image, "Scan to open WiFi")
        self.show_qr_code(save)

    def generate_mecard_qr_code(
        self,
        name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        url: Optional[str] = None,
        save: bool = False,
        custom: Path = None,
        frame_type: Optional[str] = None,
        size: int = 10,
        color: str = "#000000",
        color2: HexCode = "#FFFFFF",
        color3: HexCode = "#000000",
    ) -> None:
        """Generates a QR code for a MeCard contact."""
        logger.debug("Generating MeCard QR code for name: %s", name)
        mecard_data = (
            f"MECARD:N:{name};"
            f"EMAIL:{email};TEL:{phone};URL:{url};;"
        )
        result = self.generate_qr_code(
            data=mecard_data, custom=custom, color=color, scale=size
        )
        if frame_type:
            logger.info("Adding frame_type to QR code.")
            self.qr_image = add_frame_to_image(self.qr_image, frame_type)
        if not result:
            logger.info("Adding text to QR code image.")
            self.qr_image = add_text_to_image(self.qr_image, "Scan to view MeCard")
        self.show_qr_code(save)

    def generate_vcard_qr_code(
        self,
        name: str,
        displayname: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        color: str = "#000000",
        org: Optional[str] = None,
        url: Optional[str] = None,
        address: Optional[str] = None,
        save: bool = False,
        size: int = 10,
        custom: Path = None,
        frame_type: Optional[str] = None,
        color2: HexCode = "#FFFFFF",
        color3: HexCode = "#000000",
    ) -> None:
        """Generates a QR code for a VCard contact."""
        logger.debug("Generating VCard QR code for name: %s", name)
        vcard_data = (
            f"BEGIN:VCARD\nVERSION:3.0\nN:{name}\n"
            f"FN:{displayname}\nEMAIL:{email}\nTEL:{phone}\n"
            f"ORG:{org}\nADR:{address}\nURL:{url}\nEND:VCARD"
        )
        result = self.generate_qr_code(
            data=vcard_data,
            color=color,
            color2=color2,
            color3=color3,
            scale=size,
            custom=custom,
        )
        if frame_type:
            logger.info("Adding frame_type to QR code.")
            self.qr_image = add_frame_to_image(self.qr_image, frame_type)
        if not result:
            logger.info("Adding text to QR code image.")
            self.qr_image = add_text_to_image(self.qr_image, "Scan to view VCard")
        self.show_qr_code(save)
