import pytest
from pathlib import Path
from PIL import Image
from sage_qrcode.service.contact_qrcode import ContactQRCode

class TestContactQRCodeGeneration:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.contact_qrcode = ContactQRCode()

    @pytest.fixture
    def temp_image(self, tmpdir):
        img = Image.new('RGB', (100, 100), color='red')
        path = Path(tmpdir) / 'temp_image.png'
        img.save(path)
        return path

    def test_generate_wifi_qr_code(self):
        self.contact_qrcode.generate_wifi_qr_code(
            ssid="TestSSID",
            password="TestPassword",
            security_type="WPA",
            save=False
        )
        assert self.contact_qrcode.qr_image is not None

    @pytest.mark.parametrize("security_type", ["WPA", "WEP", None])
    def test_generate_wifi_qr_code_with_different_security_types(self, security_type):
        self.contact_qrcode.generate_wifi_qr_code(
            ssid="TestSSID",
            password="TestPassword",
            security_type=security_type,
            save=False
        )
        assert self.contact_qrcode.qr_image is not None

    def test_generate_wifi_qr_code_with_empty_ssid(self):
        self.contact_qrcode.generate_wifi_qr_code(
        ssid="",
        password="TestPassword",
        security_type="WPA",
        save=False
        )
        assert self.contact_qrcode.qr_image is not None


    def test_generate_mecard_qr_code(self):
        self.contact_qrcode.generate_mecard_qr_code(
            name="John Doe",
            email="john.doe@example.com",
            phone="+1234567890",
            url="https://example.com",
            save=False
        )
        assert self.contact_qrcode.qr_image is not None

    def test_generate_vcard_qr_code_with_full_details(self):
        self.contact_qrcode.generate_vcard_qr_code(
            name="John Doe",
            displayname="Johnny",
            email="john.doe@example.com",
            phone="+1234567890",
            org="ExampleOrg",
            url="https://example.com",
            address="123 Main St, Anytown, USA",
            save=False
        )
        assert self.contact_qrcode.qr_image is not None

    @pytest.mark.parametrize("optional_field", ["displayname", "email", "phone", "org", "url", "address"])
    def test_generate_vcard_qr_code_with_missing_optional_fields(self, optional_field):
        kwargs = {
            "name": "John Doe",
            "displayname": "Johnny",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "org": "ExampleOrg",
            "url": "https://example.com",
            "address": "123 Main St, Anytown, USA",
            "save": False
        }
        del kwargs[optional_field]
        self.contact_qrcode.generate_vcard_qr_code(**kwargs)
        assert self.contact_qrcode.qr_image is not None

    @pytest.mark.parametrize("frame_type", ["simple", "rounded"])
    def test_qr_code_with_different_frame_types(self, frame_type):
        self.contact_qrcode.generate_wifi_qr_code(
            ssid="TestSSID",
            password="TestPassword",
            security_type="WPA",
            save=False,
            frame_type=frame_type
        )
        assert self.contact_qrcode.qr_image is not None

    def test_qr_code_with_custom_image(self, temp_image):
        self.contact_qrcode.generate_wifi_qr_code(
            ssid="TestSSID",
            password="TestPassword",
            security_type="WPA",
            save=False,
            custom=temp_image
        )
        assert self.contact_qrcode.qr_image is not None
