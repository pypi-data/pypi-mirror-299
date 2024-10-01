import re
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class ValidatorE164:
    """E.164 phone number format validator.

    Validates that a phone number is in E.164 format, which allows for a maximum of fifteen digits
    and requires the number to start with a '+' symbol.

    Attributes:
        message (str): Error message to be used if validation fails.
        code (str): Error code to be used if validation fails.
        regex (Pattern): Compiled regular expression pattern for E.164 validation.

    """

    message = _("Invalid phone number format. Must be in E.164 format.")
    code = "invalid"
    regex = re.compile(r"^\+[1-9]\d{1,14}$")

    def __init__(self, message=None, code=None):
        """Initializes the ValidatorE164 with optional custom message and code.

        Args:
            message (str, optional): Custom error message.
            code (str, optional): Custom error code.

        """
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        """Validates that the provided value matches the E.164 phone number
        format.

        Args:
            value (str): The phone number to validate.

        Raises:
            ValidationError: If the value does not match the E.164 format.

        """
        if not self.regex.match(value):
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def __eq__(self, other):
        """Compares this ValidatorE164 instance with another for equality.

        Args:
            other (ValidatorE164): Another instance to compare with.

        Returns:
            bool: True if both instances have the same message and code, False otherwise.

        """
        return (
            isinstance(other, ValidatorE164)
            and self.message == other.message
            and self.code == other.code
        )


validate_e164 = ValidatorE164()
validate_phone_number = ValidatorE164()
