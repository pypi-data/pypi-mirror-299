import re
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class IBANValidator:
    """Validator for IBAN (International Bank Account Number).

    This validator checks whether a given value is a valid IBAN,
    which typically consists of a country code followed by digits and alphanumeric characters.

    Attributes:
        message (str): Error message returned when the validation fails.
        code (str): Error code returned when the validation fails.
        regex (Pattern): Compiled regular expression for validating IBANs.

    """

    message = _("Enter a valid IBAN.")
    code = "invalid"
    regex = re.compile(r"^[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}$")

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        if not self.regex.match(value):
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def __eq__(self, other):
        return (
            isinstance(other, IBANValidator)
            and self.message == other.message
            and self.code == other.code
        )


validate_iban = IBANValidator()
