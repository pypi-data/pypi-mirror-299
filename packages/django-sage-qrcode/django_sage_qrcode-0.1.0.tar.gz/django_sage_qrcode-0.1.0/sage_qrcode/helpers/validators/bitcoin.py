import re
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class BitcoinAddressValidator:
    """Validator for Bitcoin addresses.

    This validator checks whether a given value is a valid Bitcoin address.
    It uses a regular expression to match the typical structure of Bitcoin addresses,
    which start with '1' or '3' and are 26-35 characters long.

    Attributes:
        message (str): Error message returned when the validation fails.
        code (str): Error code returned when the validation fails.
        regex (Pattern): Compiled regular expression for validating Bitcoin addresses.

    """

    message = _("Enter a valid Bitcoin address.")
    code = "invalid"
    regex = re.compile(r"^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$")

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        """Validates the given Bitcoin address.

        Args:
            value (str): The Bitcoin address to validate.

        Raises:
            ValidationError: If the Bitcoin address is not valid.

        """
        if not self.regex.match(value):
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def __eq__(self, other):
        return (
            isinstance(other, BitcoinAddressValidator)
            and self.message == other.message
            and self.code == other.code
        )


validate_bitcoin_address = BitcoinAddressValidator()
