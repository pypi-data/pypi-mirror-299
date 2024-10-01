import pytest
from django.core.exceptions import ValidationError
from sage_qrcode.helpers.validators import (
    TikTokValidator,
    SnapchatValidator,
    InstagramValidator,
    FacebookValidator,
    TelegramValidator,
    LinkedInValidator,
    SkypeValidator,
)


class TestSocialMediaValidators:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.validators = {
            "tiktok": TikTokValidator(),
            "snapchat": SnapchatValidator(),
            "instagram": InstagramValidator(),
            "facebook": FacebookValidator(),
            "telegram": TelegramValidator(),
            "linkedin": LinkedInValidator(),
            "skype": SkypeValidator(),
        }

    @pytest.mark.parametrize("validator_name, url", [
        ("tiktok", "https://www.tiktok.com/@username"),
        ("tiktok", "https://tiktok.com/@user123"),
        ("snapchat", "https://www.snapchat.com/add/username"),
        ("snapchat", "https://snapchat.com/add/user123"),
        ("instagram", "https://www.instagram.com/username"),
        ("instagram", "https://instagram.com/user123"),
        ("facebook", "https://www.facebook.com/username"),
        ("facebook", "https://facebook.com/user123"),
        ("telegram", "https://t.me/username"),
        ("telegram", "https://t.me/user123"),
        ("linkedin", "https://www.linkedin.com/in/username"),
        ("linkedin", "https://linkedin.com/in/user123"),
        ("skype", "https://www.skype.com/username"),
        ("skype", "https://skype.com/user123"),
    ])
    def test_valid_social_media_urls(self, validator_name, url):
        validator = self.validators[validator_name]
        try:
            validator(url)
            assert True
        except ValidationError as e:
            pytest.fail(f"Valid {validator_name.capitalize()} URL '{url}' raised a ValidationError: {str(e)}")

    @pytest.mark.parametrize("validator_name, url", [
        ("tiktok", "https://www.tiktok.com/user123"),
        ("tiktok", "https://www.tiktok.com/@user123/extra"),
        ("snapchat", "https://www.snapchat.com/username"),
        ("snapchat", "https://snapchat.com/add/user123/extra"),
        ("instagram", "https://www.instagram.com/user123/extra"),
        ("instagram", "https://instagram.com"),
        ("facebook", "https://www.facebook.com/user123/extra"),
        ("facebook", "https://facebook.com"),
        ("telegram", "https://t.me/"),
        ("telegram", "https://t.me/user123/extra"),
        ("linkedin", "https://www.linkedin.com/"),
        ("linkedin", "https://linkedin.com/in/user123/extra"),
        ("skype", "https://www.skype.com/"),
        ("skype", "https://skype.com/user123/extra"),
        ("tiktok", "invalidurl"),
        ("snapchat", "invalidurl"),
        ("instagram", "invalidurl"),
        ("facebook", "invalidurl"),
        ("telegram", "invalidurl"),
        ("linkedin", "invalidurl"),
        ("skype", "invalidurl"),
        ("tiktok", ""),
        ("snapchat", ""),
        ("instagram", ""),
        ("facebook", ""),
        ("telegram", ""),
        ("linkedin", ""),
        ("skype", ""),
    ])
    def test_invalid_social_media_urls(self, validator_name, url):
        validator = self.validators[validator_name]
        with pytest.raises(ValidationError):
            validator(url)
