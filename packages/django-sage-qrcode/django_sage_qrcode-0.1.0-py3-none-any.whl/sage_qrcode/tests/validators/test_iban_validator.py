import pytest
from django.core.exceptions import ValidationError
from sage_qrcode.helpers.validators import IBANValidator
from django.conf import settings

@pytest.fixture(autouse=True)
def setup_django_settings():
    if not settings.configured:
        settings.configure(
            USE_I18N=True,
            USE_L10N=True,
            USE_TZ=True,
        )

class TestIBANValidator:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.validator = IBANValidator()

    @pytest.mark.parametrize("iban", [
        "DE89370400440532013000",
        "GB33BUKB20201555555555",
    ])
    def test_valid_ibans(self, iban):
        try:
            self.validator(iban)
            assert True
        except ValidationError as e:
            pytest.fail(f"Valid IBAN '{iban}' raised a ValidationError: {str(e)}")

    @pytest.mark.parametrize("iban", [
        "INVALIDIBAN",
        "INVALIDIBAN2",
        "",
    ])
    def test_invalid_ibans(self, iban):
        with pytest.raises(ValidationError):
            self.validator(iban)
