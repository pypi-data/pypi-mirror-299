import os
import logging
from pathlib import Path
from typing import Optional

from sage_qrcode.service.base import QRCodeBase
from sage_qrcode.utils import add_text_to_image, add_icon_to_image, add_frame_to_image
from sage_qrcode.helpers.type import HexCode

try:
    from PIL import Image
except ImportError as exc:
    raise ImportError("Install `pillow` package. Run `pip install pillow`.") from exc

logger = logging.getLogger(__name__)

class SocialMediaQRCode(QRCodeBase):
    """A class for generating QR codes that include social media icons and
    related functionality."""

    def add_social_media_icon(self, url: str) -> Image.Image:
        """Adds an appropriate social media icon to the QR code based on the
        provided URL.
        Args:
            url (str): The social media URL.
        Returns:
            Image.Image: The QR code image with the social media icon.
        Raises:
            ValueError: If the URL does not match any known social media platforms.
        """
        logger.debug("Attempting to add a social media icon for URL: %s", url)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        icon_paths = {
            "instagram.com": "icons/instagram.png",
            "whatsapp.com": "icons/logo.png",
            "t.me": "icons/gram.png",
            "facebook.com": "icons/meta.png",
            "twitter.com": "icons/witter.png",
            "linkedin.com": "icons/linkedin.png",
            "snapchat.com": "icons/snapchat.png",
            "tiktok.com": "icons/ti.png",
            "skype.com": "icons/skype.png",
        }

        for key, path in icon_paths.items():
            if key in url.lower():
                logger.info("Matching icon found for %s, using icon at %s.", key, path)
                image = add_icon_to_image(self.qr_image, path)
                break
        else:
            logger.error("No matching icon found for URL: %s", url)
            raise ValueError("Invalid social media link")

        logger.info("Social media icon added successfully.")
        return image

    def create_social_media_url(
        self,
        url: str,
        save: bool = False,
        frame_type: Optional[str] = None,
        color: HexCode = "#000000",
        color2: HexCode = "#FFFFFF",
        color3: HexCode = "#000000",
        size: int = 10,
    ) -> None:
        """Generates a QR code for a social media URL and adds an appropriate
        icon.
        Args:
            url (str): The social media URL.
            save (bool, optional): Whether to save the QR code image. Default is False.
            frame_type (Optional[str], optional): Kind of frame you want.
            color (str, optional): Color of the QR code. Default is '#000000'.
            color2 (str, optional): Background color of the QR code. Default is '#FFFFFF'.
            color3 (str, optional): Finder pattern color of the QR code. Default is '#000000'.
            size (int, optional): Scale factor for the QR code size. Default is 10.
        """
        logger.debug("Creating QR code for social media URL: %s", url)
        result = self.generate_qr_code(
            data=url, custom=None, color=color, scale=size, color2=color2, color3=color3
        )
        if not result:
            logger.info("QR code generated. Adding social media icon.")
            self.qr_image = self.add_social_media_icon(url)
            if frame_type:
                logger.info("Adding frame_type to QR code.")
                self.qr_image = add_frame_to_image(self.qr_image, frame_type)
            self.qr_image = add_text_to_image(
                self.qr_image, "Scan to view social media profile"
            )
        self.show_qr_code(save)

    def create_url(
        self,
        playlist_url: str,
        save: bool = False,
        custom: Path = None,
        frame_type: Optional[str] = None,
        color: HexCode = "#000000",
        size: int = 10,
        color2: HexCode = "#FFFFFF",
        color3: HexCode = "#000000",
    ) -> None:
        """Generates a QR code for a URL and adds optional customizations like
        frame_type and text.
        Args:
            playlist_url (str): The URL to encode in the QR code.
            save (bool): Whether to save the QR code image.
            custom (Optional[str], optional): Path to a custom image to overlay on the QR code. Default is None.
            frame_type (Optional[str], optional): Kind of frame you want
            color (str, optional): Color of the QR code. Default is '#000000'.
            size (int, optional): Scale factor for the QR code size. Default is 10.
            color2 (str, optional): Background color of the QR code. Default is '#FFFFFF'.
            color3 (str, optional): Finder pattern color of the QR code. Default is '#000000'.
        """
        logger.debug("Creating QR code for URL: %s", playlist_url)
        self.generate_qr_code(
            data=playlist_url,
            custom=custom,
            scale=size,
            color=color,
            color2=color2,
            color3=color3,
        )
        if frame_type:
            logger.info("Adding frame_type to QR code.")
            self.qr_image = add_frame_to_image(self.qr_image, frame_type)
        if not self.generate_qr_code:
            logger.info("Adding text to QR code image.")
            self.qr_image = add_text_to_image(
                self.qr_image, "Scan to view social media profile"
            )
            self.show_qr_code(save)
        else:
            logger.info("Displaying QR code without saving.")
            self.show_qr_code(False)
