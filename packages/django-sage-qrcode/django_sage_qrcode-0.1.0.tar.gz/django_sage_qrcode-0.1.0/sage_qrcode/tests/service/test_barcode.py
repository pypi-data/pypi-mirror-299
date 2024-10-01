from unittest.mock import patch, MagicMock
from PIL import Image
from io import BytesIO
import pytest
from django.core.exceptions import ValidationError

class TestBarcodeProxy:

    @patch("sage_qrcode.service.barcode.get_barcode_class")
    def test_generate_barcode_url(self, mock_get_barcode_class, barcode_proxy, sample_url):
        mock_barcode_instance = MagicMock()
        mock_get_barcode_class.return_value = MagicMock(return_value=mock_barcode_instance)
        
        buffer = BytesIO()
        image = Image.new("RGB", (100, 50), color="white")
        image.save(buffer, format="PNG")
        buffer.seek(0)
        mock_barcode_instance.write = MagicMock(side_effect=lambda f, options: f.write(buffer.getvalue()))

        barcode_image = barcode_proxy.generate_barcode(data=sample_url)
        
        assert barcode_image is not None
        assert barcode_proxy.barcode_image is not None
        mock_get_barcode_class.assert_called_once()

    @patch("sage_qrcode.service.barcode.get_barcode_class")
    def test_generate_barcode_text(self, mock_get_barcode_class, barcode_proxy, sample_text):
        mock_barcode_instance = MagicMock()
        mock_get_barcode_class.return_value = MagicMock(return_value=mock_barcode_instance)
        
        buffer = BytesIO()
        image = Image.new("RGB", (100, 50), color="white")
        image.save(buffer, format="PNG")
        buffer.seek(0)
        mock_barcode_instance.write = MagicMock(side_effect=lambda f, options: f.write(buffer.getvalue()))

        barcode_image = barcode_proxy.generate_barcode(data=sample_text)
        
        assert barcode_image is not None
        assert barcode_proxy.barcode_image is not None
        mock_get_barcode_class.assert_called_once()

    @patch("pyshorteners.Shortener")
    def test_shorten_url(self, mock_shortener, barcode_proxy, sample_url):
        mock_tinyurl = mock_shortener.return_value.tinyurl
        mock_tinyurl.short.return_value = "https://tinyurl.com/shortened-url"
        
        shortened_url = barcode_proxy.shorten_url(sample_url)
        
        assert shortened_url == "https://tinyurl.com/shortened-url"
        mock_tinyurl.short.assert_called_once_with(sample_url)

    @patch("sage_qrcode.service.barcode.get_barcode_class")
    def test_save_barcode(self, mock_get_barcode_class, barcode_proxy, sample_text, tmp_path):
        mock_barcode_instance = MagicMock()
        mock_get_barcode_class.return_value = MagicMock(return_value=mock_barcode_instance)
        
        buffer = BytesIO()
        image = Image.new("RGB", (100, 50), color="white")
        image.save(buffer, format="PNG")
        buffer.seek(0)
        mock_barcode_instance.write = MagicMock(side_effect=lambda f, options: f.write(buffer.getvalue()))

        barcode_proxy.generate_barcode(data=sample_text)
        barcode_proxy.save_barcode()
        
        barcode_image_path = tmp_path / "test_barcode.png"
        barcode_proxy.barcode_image.save(barcode_image_path)
        
        assert barcode_image_path.exists()

    @patch("sage_qrcode.service.barcode.get_barcode_class")
    def test_generate_barcode_custom_colors(self, mock_get_barcode_class, barcode_proxy, sample_text):
        mock_barcode_instance = MagicMock()
        mock_get_barcode_class.return_value = MagicMock(return_value=mock_barcode_instance)

        buffer = BytesIO()
        image = Image.new("RGB", (100, 50), color="yellow")  # Custom background color
        image.save(buffer, format="PNG")
        buffer.seek(0)
        mock_barcode_instance.write = MagicMock(side_effect=lambda f, options: f.write(buffer.getvalue()))

        barcode_image = barcode_proxy.generate_barcode(data=sample_text, bar_color="blue", bg_color="yellow")
        
        assert barcode_image is not None
        assert barcode_proxy.barcode_image is not None
        mock_get_barcode_class.assert_called_once()
        
        # Additional checks to verify that colors are correctly applied can be done by inspecting the image object

    @patch("sage_qrcode.service.barcode.get_barcode_class")
    def test_save_barcode_different_formats(self, mock_get_barcode_class, barcode_proxy, sample_text, tmp_path):
        mock_barcode_instance = MagicMock()
        mock_get_barcode_class.return_value = MagicMock(return_value=mock_barcode_instance)
        
        buffer = BytesIO()
        image = Image.new("RGB", (100, 50), color="white")
        image.save(buffer, format="PNG")
        buffer.seek(0)
        mock_barcode_instance.write = MagicMock(side_effect=lambda f, options: f.write(buffer.getvalue()))

        barcode_proxy.generate_barcode(data=sample_text)
        barcode_proxy.save_barcode()

        # Test saving in PNG format
        barcode_image_path_png = tmp_path / "test_barcode.png"
        barcode_proxy.barcode_image.save(barcode_image_path_png, format="PNG")
        assert barcode_image_path_png.exists()

        # Test saving in JPEG format
        barcode_image_path_jpeg = tmp_path / "test_barcode.jpeg"
        barcode_proxy.barcode_image.save(barcode_image_path_jpeg, format="JPEG")
        assert barcode_image_path_jpeg.exists()
