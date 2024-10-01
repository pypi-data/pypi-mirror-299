import pytest
from django.core.exceptions import ValidationError
from sage_qrcode.helpers.validators.event import EventTimeRangeValidator
from django.conf import settings


class TestEventTimeValidator:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.validator = EventTimeRangeValidator()

    @pytest.mark.parametrize("start_time, end_time", [
        ("10:00", "11:00"),
    ])
    def test_valid_event_times(self, start_time, end_time):
        try:
            self.validator(start_time, end_time)
            assert True
        except ValidationError as e:
            pytest.fail(f"Valid event time range '{start_time} - {end_time}' raised a ValidationError: {str(e)}")

    @pytest.mark.parametrize("start_time, end_time", [
        ("11:00", "10:00"),
        ("10:00", "10:00"),
        ("invalid", "11:00"),
    ])
    def test_invalid_event_times(self, start_time, end_time):
        with pytest.raises(ValidationError):
            self.validator(start_time, end_time)
