import logging
from typing import Optional
from urllib.parse import urlencode
from pathlib import Path

from sage_qrcode.service.base import QRCodeBase
from sage_qrcode.utils import add_text_to_image, add_frame_to_image
from sage_qrcode.helpers.type import HexCode, IBAN

logger = logging.getLogger(__name__)

class PaymentQRCode(QRCodeBase):
    """
    A class for generating payment-related QR codes, 
    such as EPC and Bitcoin payment QR codes.
    """

    def generate_epc_qr_code(
        self,
        name: str,
        iban: IBAN,
        amount: float,
        text: str = "",
        save: bool = False,
        custom: Path = None,
        frame_type: Optional[str] = None,
        color: HexCode = "#000000",
        size: int = 10,
        color2: HexCode = "#FFFFFF",
        color3: HexCode = "#000000",
    ) -> None:
        """Generates a QR code for EPC (European Payments Council) payments."""
        logger.debug(
            "Generating EPC QR code for recipient: %s, IBAN: %s, Amount: %.2f",
            name, iban, amount
        )
        epc_data = (
            f"BCD\n001\n1\nSCT\n{name}\n{iban}\n"
            f"EUR{amount}\n{int(amount * 100)}\n{text}\n"
        )
        result = self.generate_qr_code(
            data=epc_data,
            custom=custom,
            color=color,
            scale=size,
            color2=color2,
            color3=color3,
        )
        if frame_type:
            logger.info("Adding frame_type to QR code.")
            self.qr_image = add_frame_to_image(self.qr_image, frame_type)
        if not result:
            logger.info("Adding text to QR code image.")
            self.qr_image = add_text_to_image(self.qr_image, "Scan for EPC payment")
        self.show_qr_code(save)

    def generate_bitcoin_qr_code(
        self,
        address: str,
        amount: Optional[float] = None,
        label: Optional[str] = None,
        save: bool = False,
        message: Optional[str] = None,
        scale: int = 10,
        color: HexCode = "#000000",
        frame_type: Optional[str] = None,
        color2: HexCode = "#FFFFFF",
        color3: HexCode = "#000000",
    ) -> None:
        """Generates a QR code for Bitcoin payments."""
        logger.debug(
            "Generating Bitcoin QR code for address: %s, Amount: %s, Label: %s",
            address, amount, label
        )
        params = {
            "amount": amount,
            "label": label,
            "message": message,
        }
        filtered_params = {k: v for k, v in params.items() if v is not None}
        query_string = urlencode(filtered_params)
        bitcoin_uri = f"bitcoin:{address}"
        if query_string:
            bitcoin_uri += f"?{query_string}"

        result = self.generate_qr_code(
            data=bitcoin_uri,
            scale=scale,
            color=color,
            color2=color2,
            color3=color3,
        )
        if frame_type:
            logger.info("Adding frame_type to QR code.")
            self.qr_image = add_frame_to_image(self.qr_image, frame_type)
        if not result:
            logger.info("Adding text to QR code image.")
            self.qr_image = add_text_to_image(
                self.qr_image, "Scan for bitcoin payment"
            )
        self.show_qr_code(save)
