import re
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class TikTokValidator:
    """Validator for TikTok profile URLs.

    Ensures that the provided URL is a valid TikTok profile URL based on a specific regex pattern.

    Attributes:
        message (str): Error message returned if the validation fails.
        code (str): Error code returned if the validation fails.
        regex (Pattern): Compiled regular expression pattern for TikTok URL validation.

    """

    message = _("Enter a valid TikTok profile URL.")
    code = "invalid"
    regex = re.compile(
        r"^https?://(?:www\.)?tiktok\.com/@[A-Za-z0-9_.-]+/?$", re.IGNORECASE
    )

    def __init__(self, message=None, code=None):
        """Initializes the TikTokValidator with optional custom message and
        code.

        Args:
            message (str, optional): Custom error message.
            code (str, optional): Custom error code.

        """
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        """Validates that the provided value matches the TikTok profile URL
        pattern.

        Args:
            value (str): The TikTok profile URL to validate.

        Raises:
            ValidationError: If the value does not match the regex pattern.

        """
        if not self.regex.match(value):
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def __eq__(self, other):
        """Compares this TikTokValidator instance with another for equality.

        Args:
            other (TikTokValidator): Another instance to compare with.

        Returns:
            bool: True if both instances have the same message and code, False otherwise.

        """
        return (
            isinstance(other, TikTokValidator)
            and self.message == other.message
            and self.code == other.code
        )


@deconstructible
class SnapchatValidator:
    """Validator for Snapchat profile URLs.

    Ensures that the provided URL is a valid Snapchat profile URL based on a specific regex pattern.

    Attributes:
        message (str): Error message returned if the validation fails.
        code (str): Error code returned if the validation fails.
        regex (Pattern): Compiled regular expression pattern for Snapchat URL validation.

    """

    message = _("Enter a valid Snapchat profile URL.")
    code = "invalid"
    regex = re.compile(
        r"^https?://(?:www\.)?snapchat\.com/add/[A-Za-z0-9_.-]+/?$", re.IGNORECASE
    )

    def __init__(self, message=None, code=None):
        """Initializes the SnapchatValidator with optional custom message and
        code.

        Args:
            message (str, optional): Custom error message.
            code (str, optional): Custom error code.

        """
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        """Validates that the provided value matches the Snapchat profile URL
        pattern.

        Args:
            value (str): The Snapchat profile URL to validate.

        Raises:
            ValidationError: If the value does not match the regex pattern.

        """
        if not self.regex.match(value):
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def __eq__(self, other):
        """Compares this SnapchatValidator instance with another for equality.

        Args:
            other (SnapchatValidator): Another instance to compare with.

        Returns:
            bool: True if both instances have the same message and code, False otherwise.

        """
        return (
            isinstance(other, SnapchatValidator)
            and self.message == other.message
            and self.code == other.code
        )


@deconstructible
class InstagramValidator:
    """Validator for Instagram profile URLs.

    Ensures that the provided URL is a valid Instagram profile URL based on a specific regex pattern.

    Attributes:
        message (str): Error message returned if the validation fails.
        code (str): Error code returned if the validation fails.
        regex (Pattern): Compiled regular expression pattern for Instagram URL validation.

    """

    message = _("Enter a valid Instagram profile URL.")
    code = "invalid"
    regex = re.compile(
        r"^https?://(?:www\.)?instagram\.com/[A-Za-z0-9_.-]+/?$", re.IGNORECASE
    )

    def __init__(self, message=None, code=None):
        """Initializes the InstagramValidator with optional custom message and
        code.

        Args:
            message (str, optional): Custom error message.
            code (str, optional): Custom error code.

        """
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        """Validates that the provided value matches the Instagram profile URL
        pattern.

        Args:
            value (str): The Instagram profile URL to validate.

        Raises:
            ValidationError: If the value does not match the regex pattern.

        """
        if not self.regex.match(value):
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def __eq__(self, other):
        """Compares this InstagramValidator instance with another for equality.

        Args:
            other (InstagramValidator): Another instance to compare with.

        Returns:
            bool: True if both instances have the same message and code, False otherwise.

        """
        return (
            isinstance(other, InstagramValidator)
            and self.message == other.message
            and self.code == other.code
        )


@deconstructible
class FacebookValidator:
    """Validator for Facebook profile URLs.

    Ensures that the provided URL is a valid Facebook profile URL based on a specific regex pattern.

    Attributes:
        message (str): Error message returned if the validation fails.
        code (str): Error code returned if the validation fails.
        regex (Pattern): Compiled regular expression pattern for Facebook URL validation.

    """

    message = _("Enter a valid Facebook profile URL.")
    code = "invalid"
    regex = re.compile(
        r"^https?://(?:www\.)?facebook\.com/[A-Za-z0-9_.-]+/?$", re.IGNORECASE
    )

    def __init__(self, message=None, code=None):
        """Initializes the FacebookValidator with optional custom message and
        code.

        Args:
            message (str, optional): Custom error message.
            code (str, optional): Custom error code.

        """
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        """Validates that the provided value matches the Facebook profile URL
        pattern.

        Args:
            value (str): The Facebook profile URL to validate.

        Raises:
            ValidationError: If the value does not match the regex pattern.

        """
        if not self.regex.match(value):
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def __eq__(self, other):
        """Compares this FacebookValidator instance with another for equality.

        Args:
            other (FacebookValidator): Another instance to compare with.

        Returns:
            bool: True if both instances have the same message and code, False otherwise.

        """
        return (
            isinstance(other, FacebookValidator)
            and self.message == other.message
            and self.code == other.code
        )


@deconstructible
class TelegramValidator:
    """Validator for Telegram profile URLs.

    Ensures that the provided URL is a valid Telegram profile URL based on a specific regex pattern.

    Attributes:
        message (str): Error message returned if the validation fails.
        code (str): Error code returned if the validation fails.
        regex (Pattern): Compiled regular expression pattern for Telegram URL validation.

    """

    message = _("Enter a valid Telegram profile URL.")
    code = "invalid"
    regex = re.compile(r"^https?://t\.me/[A-Za-z0-9_]+/?$", re.IGNORECASE)

    def __init__(self, message=None, code=None):
        """Initializes the TelegramValidator with optional custom message and
        code.

        Args:
            message (str, optional): Custom error message.
            code (str, optional): Custom error code.

        """
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        """Validates that the provided value matches the Telegram profile URL
        pattern.

        Args:
            value (str): The Telegram profile URL to validate.

        Raises:
            ValidationError: If the value does not match the regex pattern.

        """
        if not self.regex.match(value):
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def __eq__(self, other):
        """Compares this TelegramValidator instance with another for equality.

        Args:
            other (TelegramValidator): Another instance to compare with.

        Returns:
            bool: True if both instances have the same message and code, False otherwise.

        """
        return (
            isinstance(other, TelegramValidator)
            and self.message == other.message
            and self.code == other.code
        )


@deconstructible
class LinkedInValidator:
    """Validator for LinkedIn profile URLs.

    Ensures that the provided URL is a valid LinkedIn profile URL based on a specific regex pattern.

    Attributes:
        message (str): Error message returned if the validation fails.
        code (str): Error code returned if the validation fails.
        regex (Pattern): Compiled regular expression pattern for LinkedIn URL validation.

    """

    message = _("Enter a valid LinkedIn profile URL.")
    code = "invalid"
    regex = re.compile(
        r"^https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?$", re.IGNORECASE
    )

    def __init__(self, message=None, code=None):
        """Initializes the LinkedInValidator with optional custom message and
        code.

        Args:
            message (str, optional): Custom error message.
            code (str, optional): Custom error code.

        """
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        """Validates that the provided value matches the LinkedIn profile URL
        pattern.

        Args:
            value (str): The LinkedIn profile URL to validate.

        Raises:
            ValidationError: If the value does not match the regex pattern.

        """
        if not self.regex.match(value):
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def __eq__(self, other):
        """Compares this LinkedInValidator instance with another for equality.

        Args:
            other (LinkedInValidator): Another instance to compare with.

        Returns:
            bool: True if both instances have the same message and code, False otherwise.

        """
        return (
            isinstance(other, LinkedInValidator)
            and self.message == other.message
            and self.code == other.code
        )


@deconstructible
class XValidator:
    """Validator for X (formerly Twitter) profile URLs.

    Ensures that the provided URL is a valid X profile URL based on a specific regex pattern.

    Attributes:
        message (str): Error message returned if the validation fails.
        code (str): Error code returned if the validation fails.
        regex (Pattern): Compiled regular expression pattern for X URL validation.

    """

    message = _("Enter a valid X profile URL.")
    code = "invalid"
    regex = re.compile(
        r"^https?://(?:www\.)?twitter\.com/[A-Za-z0-9_]+/?$", re.IGNORECASE
    )

    def __init__(self, message=None, code=None):
        """Initializes the XValidator with optional custom message and code.

        Args:
            message (str, optional): Custom error message.
            code (str, optional): Custom error code.

        """
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        """Validates that the provided value matches the X profile URL pattern.

        Args:
            value (str): The X profile URL to validate.

        Raises:
            ValidationError: If the value does not match the regex pattern.

        """
        if not self.regex.match(value):
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def __eq__(self, other):
        """Compares this XValidator instance with another for equality.

        Args:
            other (XValidator): Another instance to compare with.

        Returns:
            bool: True if both instances have the same message and code, False otherwise.

        """
        return (
            isinstance(other, XValidator)
            and self.message == other.message
            and self.code == other.code
        )


@deconstructible
class SkypeValidator:
    """Validator for Skype profile URLs.

    Ensures that the provided URL is a valid Skype profile URL based on a specific regex pattern.

    Attributes:
        message (str): Error message returned if the validation fails.
        code (str): Error code returned if the validation fails.
        regex (Pattern): Compiled regular expression pattern for Skype URL validation.

    """

    message = _("Enter a valid Skype profile URL.")
    code = "invalid"
    regex = re.compile(
        r"^https?://(?:www\.)?skype\.com/[A-Za-z0-9_.-]+/?$", re.IGNORECASE
    )

    def __init__(self, message=None, code=None):
        """Initializes the SkypeValidator with optional custom message and
        code.

        Args:
            message (str, optional): Custom error message.
            code (str, optional): Custom error code.

        """
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        """Validates that the provided value matches the Skype profile URL
        pattern.

        Args:
            value (str): The Skype profile URL to validate.

        Raises:
            ValidationError: If the value does not match the regex pattern.

        """
        if not self.regex.match(value):
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def __eq__(self, other):
        """Compares this SkypeValidator instance with another for equality.

        Args:
            other (SkypeValidator): Another instance to compare with.

        Returns:
            bool: True if both instances have the same message and code, False otherwise.

        """
        return (
            isinstance(other, SkypeValidator)
            and self.message == other.message
            and self.code == other.code
        )


validate_instagram = InstagramValidator()
validate_snapchat = SnapchatValidator()
validate_facebook = FacebookValidator()
validate_telegram = TelegramValidator()
validate_linkedin = LinkedInValidator()
validate_tiktok = TikTokValidator()
validate_skype = SkypeValidator()
validate_x = XValidator()
