import pytest
from django.core.exceptions import ValidationError
from sage_qrcode.helpers.validators import BitcoinAddressValidator
from django.conf import settings

@pytest.fixture(autouse=True)
def setup_django_settings():
    if not settings.configured:
        settings.configure(
            USE_I18N=True,
            USE_L10N=True,
            USE_TZ=True,
        )

class TestBitcoinAddressValidator:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.validator = BitcoinAddressValidator()

    @pytest.mark.parametrize("address", [
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",
    ])
    def test_valid_bitcoin_addresses(self, address):
        try:
            self.validator(address)
            assert True
        except ValidationError as e:
            pytest.fail(f"Valid Bitcoin address '{address}' raised a ValidationError: {str(e)}")

    @pytest.mark.parametrize("address", [
        "1A1zP1eP5QGefi2D",
        "mQviecrnyiWrnqRhWNLyy",
        "invalidbitcoinaddress", 
        "",
    ])
    def test_invalid_bitcoin_addresses(self, address):
        with pytest.raises(ValidationError):
            self.validator(address)
