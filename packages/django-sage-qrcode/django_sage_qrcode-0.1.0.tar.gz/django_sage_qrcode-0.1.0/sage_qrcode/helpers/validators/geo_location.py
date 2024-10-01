from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class LatitudeValidator:
    """Validator for latitude values.

    This validator checks whether a given value is a valid latitude,
    which must be between -90 and 90.

    Attributes:
        message (str): Error message returned when the validation fails.
        code (str): Error code returned when the validation fails.

    """

    message = _("Enter a valid latitude between -90 and 90.")
    code = "invalid"

    def __call__(self, value):
        """Validates the latitude value.

        Args:
            value (float): The latitude value to validate.

        Raises:
            ValidationError: If the latitude is not between -90 and 90.

        """
        if value < -90 or value > 90:
            raise ValidationError(self.message, code=self.code, params={"value": value})


@deconstructible
class LongitudeValidator:
    """Validator for longitude values.

    This validator checks whether a given value is a valid longitude,
    which must be between -180 and 180.

    Attributes:
        message (str): Error message returned when the validation fails.
        code (str): Error code returned when the validation fails.

    """

    message = _("Enter a valid longitude between -180 and 180.")
    code = "invalid"

    def __call__(self, value):
        """Validates the longitude value.

        Args:
            value (float): The longitude value to validate.

        Raises:
            ValidationError: If the longitude is not between -180 and 180.

        """
        if value < -180 or value > 180:
            raise ValidationError(self.message, code=self.code, params={"value": value})


validate_latitude = LatitudeValidator()
validate_longitude = LongitudeValidator()
