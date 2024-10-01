import pytest
from pathlib import Path
from sage_qrcode.service.payment_qrcode import PaymentQRCode
from PIL import Image

class TestPaymentQRCodeGeneration:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.payment_qrcode = PaymentQRCode()

    def test_generate_epc_qr_code(self):
        self.payment_qrcode.generate_epc_qr_code(
            name="John Doe",
            iban="DE89370400440532013000",
            amount=100.00,
            text="Payment for Invoice 123",
            save=False
        )
        assert self.payment_qrcode.qr_image is not None

    def test_generate_epc_qr_code_without_text(self):
        self.payment_qrcode.generate_epc_qr_code(
            name="John Doe",
            iban="DE89370400440532013000",
            amount=100.00,
            save=False
        )
        assert self.payment_qrcode.qr_image is not None

    def test_generate_bitcoin_qr_code(self):
        self.payment_qrcode.generate_bitcoin_qr_code(
            address="1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
            amount=0.001,
            label="Donation",
            save=False
        )
        assert self.payment_qrcode.qr_image is not None

    def test_generate_bitcoin_qr_code_with_address_only(self):
        self.payment_qrcode.generate_bitcoin_qr_code(
            address="1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
            save=False
        )
        assert self.payment_qrcode.qr_image is not None

    @pytest.mark.parametrize("frame_type", ["simple", "rounded"])
    def test_epc_qr_code_with_frame_and_text(self, frame_type):
        self.payment_qrcode.generate_epc_qr_code(
            name="John Doe",
            iban="DE89370400440532013000",
            amount=100.00,
            text="Payment for Invoice 123",
            save=False,
            frame_type=frame_type
        )
        assert self.payment_qrcode.qr_image is not None

    def test_epc_qr_code_with_custom_text(self):
        self.payment_qrcode.generate_epc_qr_code(
            name="John Doe",
            iban="DE89370400440532013000",
            amount=100.00,
            text="Payment for Invoice 123",
            save=False
        )
        assert self.payment_qrcode.qr_image is not None

    @pytest.mark.parametrize("frame_type", ["simple", "rounded"])
    def test_bitcoin_qr_code_with_frame_and_text(self, frame_type):
        self.payment_qrcode.generate_bitcoin_qr_code(
            address="1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
            amount=0.001,
            label="Donation",
            save=False,
            frame_type=frame_type
        )
        assert self.payment_qrcode.qr_image is not None

    def test_bitcoin_qr_code_with_custom_text(self):
        self.payment_qrcode.generate_bitcoin_qr_code(
            address="1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
            amount=0.001,
            label="Donation",
            save=False
        )
        assert self.payment_qrcode.qr_image is not None
