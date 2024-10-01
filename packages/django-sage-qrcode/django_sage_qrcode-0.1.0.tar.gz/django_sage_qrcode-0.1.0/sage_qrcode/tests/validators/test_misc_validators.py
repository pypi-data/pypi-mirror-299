import pytest
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from sage_qrcode.helpers.validators import (
    ImageFileValidator,
    SizeValidator,
    LatitudeValidator,
    LongitudeValidator,
)


class TestMiscValidators:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.image_validator = ImageFileValidator()
        self.size_validator = SizeValidator()
        self.latitude_validator = LatitudeValidator()
        self.longitude_validator = LongitudeValidator()

    @pytest.mark.parametrize("file_data, max_size, should_raise", [
        (SimpleUploadedFile("test.jpg", b"image data", content_type="image/jpeg"), None, False),  # Valid image, no size limit
        (SimpleUploadedFile("test.jpg", b"image data", content_type="image/jpeg"), 1024, False),  # Valid image, within size limit
    ])
    def test_image_file_validator(self, file_data, max_size, should_raise):
        validator = ImageFileValidator(max_size=max_size)
        if should_raise:
            with pytest.raises(ValidationError):
                validator(file_data)
        else:
            try:
                validator(file_data)
                assert True
            except ValidationError as e:
                pytest.fail(f"Valid image file '{file_data.name}' raised a ValidationError: {str(e)}")

    @pytest.mark.parametrize("value, should_raise", [
        (500, False),  # Valid size
        (1, False),  # Boundary case (min)
        (1000, False),  # Boundary case (max)
        (0, True),  # Below min
        (1001, True),  # Above max
    ])
    def test_size_validator(self, value, should_raise):
        if should_raise:
            with pytest.raises(ValidationError):
                self.size_validator(value)
        else:
            try:
                self.size_validator(value)
                assert True
            except ValidationError as e:
                pytest.fail(f"Valid size '{value}' raised a ValidationError: {str(e)}")

    @pytest.mark.parametrize("latitude, should_raise", [
        (45.0, False),  # Valid latitude
        (-90.0, False),  # Boundary case (min)
        (90.0, False),  # Boundary case (max)
        (-91.0, True),  # Below min
        (91.0, True),  # Above max
    ])
    def test_latitude_validator(self, latitude, should_raise):
        if should_raise:
            with pytest.raises(ValidationError):
                self.latitude_validator(latitude)
        else:
            try:
                self.latitude_validator(latitude)
                assert True
            except ValidationError as e:
                pytest.fail(f"Valid latitude '{latitude}' raised a ValidationError: {str(e)}")

    @pytest.mark.parametrize("longitude, should_raise", [
        (90.0, False),
        (-180.0, False),
        (180.0, False), 
        (-181.0, True),
        (181.0, True),  
    ])
    def test_longitude_validator(self, longitude, should_raise):
        if should_raise:
            with pytest.raises(ValidationError):
                self.longitude_validator(longitude)
        else:
            try:
                self.longitude_validator(longitude)
                assert True
            except ValidationError as e:
                pytest.fail(f"Valid longitude '{longitude}' raised a ValidationError: {str(e)}")
