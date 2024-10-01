from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from django.core.files.images import get_image_dimensions


@deconstructible
class ImageFileValidator:
    """Validator for image files.

    Ensures that the uploaded file is a valid image file and optionally checks the file size
    against a specified maximum limit.

    Attributes:
        message (str): The error message to be returned if validation fails.
        code (str): The error code to be used if validation fails.
        max_size (int, optional): The maximum file size allowed in bytes.

    """

    message = _("Upload a valid image file.")
    code = "invalid"
    max_size = None  # Max size in bytes

    def __init__(self, message=None, code=None, max_size=None):
        """Initializes the ImageFileValidator with optional custom message,
        code, and maximum size.

        Args:
            message (str, optional): Custom error message.
            code (str, optional): Custom error code.
            max_size (int, optional): Maximum allowed file size in bytes.

        """
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if max_size is not None:
            self.max_size = max_size

    def __call__(self, value):
        """Validates that the uploaded file is a valid image and optionally
        checks its size.

        Args:
            value (File): The uploaded file to validate.

        Raises:
            ValidationError: If the file is not a valid image or exceeds the maximum allowed size.

        """
        # Check if the file is an image
        try:
            width, height = get_image_dimensions(value)
        except Exception:
            raise ValidationError(self.message, code=self.code)

        # Check the file size
        if self.max_size and value.size > self.max_size:
            raise ValidationError(
                _("File size should be under %(max_size)d bytes.")
                % {"max_size": self.max_size},
                code=self.code,
            )

    def __eq__(self, other):
        """Compares this ImageFileValidator instance with another for equality.

        Args:
            other (ImageFileValidator): Another instance to compare with.

        Returns:
            bool: True if both instances have the same message, code, and max_size, False otherwise.

        """
        return (
            isinstance(other, ImageFileValidator)
            and self.message == other.message
            and self.code == other.code
            and self.max_size == other.max_size
        )


@deconstructible
class SizeValidator:
    """Validator for a numerical size field.

    Ensures that the size value is within a specified range.

    Attributes:
        message (str): The error message to be returned if validation fails.
        code (str): The error code to be used if validation fails.
        min_value (int): The minimum allowed value for the size.
        max_value (int): The maximum allowed value for the size.

    """

    message = _("Size must be between 1 and 1000.")
    code = "invalid"
    min_value = 1
    max_value = 1000

    def __init__(self, message=None, code=None, min_value=None, max_value=None):
        """Initializes the SizeValidator with optional custom message, code,
        minimum, and maximum values.

        Args:
            message (str, optional): Custom error message.
            code (str, optional): Custom error code.
            min_value (int, optional): Minimum allowed value.
            max_value (int, optional): Maximum allowed value.

        """
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if min_value is not None:
            self.min_value = min_value
        if max_value is not None:
            self.max_value = max_value

    def __call__(self, value):
        """Validates that the size value is within the specified range.

        Args:
            value (int): The size value to validate.

        Raises:
            ValidationError: If the value is outside the specified range.

        """
        if value is not None and (value < self.min_value or value > self.max_value):
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def __eq__(self, other):
        """Compares this SizeValidator instance with another for equality.

        Args:
            other (SizeValidator): Another instance to compare with.

        Returns:
            bool: True if both instances have the same message, code, min_value, and max_value, False otherwise.

        """
        return (
            isinstance(other, SizeValidator)
            and self.message == other.message
            and self.code == other.code
            and self.min_value == other.min_value
            and self.max_value == other.max_value
        )


validate_size = SizeValidator()
validate_image_file = ImageFileValidator()
