import pytest
from pathlib import Path
from sage_qrcode.service.social_qrcode import SocialMediaQRCode

class TestSocialMediaQRCodeGeneration:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.social_qrcode = SocialMediaQRCode()

    @pytest.mark.parametrize("social_url, icon_name", [
        ("https://www.instagram.com/username", "icons/instagram.png"),
        ("https://www.facebook.com/username", "icons/meta.png"),
        ("https://www.linkedin.com/in/username", "icons/linkedin.png"),
    ])
    def test_generate_social_media_qr_code(self, social_url, icon_name):
        self.social_qrcode.create_social_media_url(
            url=social_url,
            save=False
        )
        assert self.social_qrcode.qr_image is not None

    def test_unsupported_social_media_url(self):
        with pytest.raises(ValueError) as exc_info:
            self.social_qrcode.create_social_media_url(
                url="https://unsupported.com/username",
                save=False
            )
        assert str(exc_info.value) == "Invalid social media link"
