import uuid
from io import BytesIO
import logging
from typing import Optional
from barcode import get_barcode_class
from barcode.writer import ImageWriter
import pyshorteners
from sage_qrcode.helpers.type import ColorName

try:
    from PIL import Image
except ImportError as exc:
    raise ImportError("Install `pillow` package. Run `pip install pillow`.") from exc

logger = logging.getLogger(__name__)

class BarcodeProxy:
    """A proxy class for generating and handling barcodes.

    Attributes:
        barcode_image (Optional[Image.Image]): Stores the generated barcode image.
    """

    def __init__(self) -> None:
        """Initializes a new instance of BarcodeProxy with no barcode image."""
        logger.info("Initializing BarcodeProxy instance.")
        self.barcode_image: Optional[Image.Image] = None

    def shorten_url(self, url: str) -> str:
        """Shortens the provided URL using the TinyURL service.

        Args:
            url (str): The URL to shorten.

        Returns:
            str: The shortened URL.
        """
        logger.debug("Shortening URL: %s", url)
        shortener = pyshorteners.Shortener()
        shortened_url = shortener.tinyurl.short(url)
        logger.info("Shortened URL: %s", shortened_url)
        return shortened_url

    def generate_barcode(
        self,
        data: str,
        barcode_type: str = "code128",
        scale: int = 1,  # Even though 'scale' is not used, we keep it for the signature
        bar_color: ColorName = "black",
        bg_color: ColorName = "white",
    ) -> Image.Image:
        """Generates a barcode image with the specified parameters.

        Args:
            data (str): The data to encode in the barcode.
            barcode_type (str, optional): The type of barcode to generate. Default is "code128".
            scale (int, optional): The scale of the barcode image. Default is 1.
            bar_color (str, optional): The color of the bars in the barcode. Default is "black".
            bg_color (str, optional): The background color of the barcode. Default is "white".

        Returns:
            Image.Image: The generated barcode image.
        """
        logger.debug("Generating barcode with data: %s", data)

        # Shorten URLs if necessary
        if data.startswith(("http://", "https://")) and len(data) > 80:
            logger.info("Data is a long URL, shortening it...")
            data = self.shorten_url(data)

        barcode_class = get_barcode_class(barcode_type)
        barcode_instance = barcode_class(data, writer=ImageWriter())
        buffer = BytesIO()
        barcode_instance.write(
            buffer,
            options={
                "write_text": True,
                "module_width": 0.2,
                "module_height": 10.0,
                "quiet_zone": 2.0,
                "foreground": bar_color,
                "background": bg_color,
            },
        )
        buffer.seek(0)
        self.barcode_image = Image.open(buffer)

        logger.info("Barcode generated successfully.")
        return self.barcode_image

    def show_barcode(self, save: bool) -> Image.Image:
        """Displays the generated barcode image.

        Args:
            save (bool): Whether to save the barcode image to a file.

        Returns:
            Image.Image: The displayed barcode image.
        """
        logger.debug("Attempting to display barcode.")
        if self.barcode_image is None:
            logger.error("No barcode image to display.")
            raise ValueError("Barcode image is not generated.")
        if save:
            logger.info("Saving barcode image.")
            self.save_barcode()
        # self.barcode_image.show()  # Assuming this line is commented out intentionally
        logger.info("Barcode displayed successfully.")
        return self.barcode_image

    def save_barcode(self) -> None:
        """Saves the generated barcode image to a file with a unique filename."""
        logger.debug("Attempting to save barcode image.")
        if self.barcode_image is None:
            logger.error("No barcode image to save.")
            raise ValueError("Barcode image is not generated.")
        unique_filename = f"{uuid.uuid4()}.png"
        self.barcode_image.save(unique_filename)
        logger.info("Barcode image saved as %s", unique_filename)

    def create_url(
        self,
        url: str,
        save: bool = False,
        bar_color: ColorName = "black",
        bg_color: ColorName = "white",
    ) -> None:
        """Generates and displays a barcode for a given URL.

        Args:
            url (str): The URL to encode in the barcode.
            save (bool, optional): Whether to save the barcode image to a file. Default is False.
            bar_color (str, optional): The color of the bars in the barcode. Default is "black".
            bg_color (str, optional): The background color of the barcode. Default is "white".
        """
        logger.info("Creating barcode for URL: %s", url)
        self.generate_barcode(data=url, bar_color=bar_color, bg_color=bg_color)
        self.show_barcode(save)

    def create_text_barcode(
        self,
        text: str,
        save: bool = False,
        bar_color: str = "black",
        bg_color: str = "white",
    ) -> None:
        """Generates and displays a barcode for a given text.

        Args:
            text (str): The text to encode in the barcode.
            save (bool, optional): Whether to save the barcode image to a file. Default is False.
            bar_color (str, optional): The color of the bars in the barcode. Default is "black".
            bg_color (str, optional): The background color of the barcode. Default is "white".
        """
        logger.info("Creating barcode for text: %s", text)
        self.generate_barcode(data=text, bar_color=bar_color, bg_color=bg_color)
        self.show_barcode(save)
