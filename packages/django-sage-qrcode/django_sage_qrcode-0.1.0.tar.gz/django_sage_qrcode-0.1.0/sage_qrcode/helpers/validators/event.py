from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class EventTimeRangeValidator:
    """Validator to ensure that the end time is after the start time for
    events.

    This validator checks that the end time of an event is after the
    start time, ensuring that events have a valid time range.

    """

    message = _("End time must be after start time.")
    code = "invalid_time_range"

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, start_time, end_time):
        """Validates that the end time is after the start time.

        Args:
            start_time (datetime): The start time of the event.
            end_time (datetime): The end time of the event.

        Raises:
            ValidationError: If the end time is not after the start time.

        """
        if end_time <= start_time:
            raise ValidationError(
                self.message,
                code=self.code,
                params={"start_time": start_time, "end_time": end_time},
            )

    def __eq__(self, other):
        return (
            isinstance(other, EventTimeRangeValidator)
            and self.message == other.message
            and self.code == other.code
        )


validate_event_time_range = EventTimeRangeValidator()
