from PIL import Image
from sage_qrcode.utils import add_text_to_image, add_icon_to_image, add_frame_to_image

class TestAddTextToImage:

    def test_add_text_to_image(self):
        image = Image.new("RGB", (200, 200), color="white")
        result_image = add_text_to_image(image, "Test Text")
        assert result_image is not None
        assert isinstance(result_image, Image.Image)


class TestAddIconToImage:

    def test_add_icon_to_image(self, tmp_path):
        image = Image.new("RGBA", (200, 200), color="white")
        icon_path = tmp_path / "test_icon.png"
        icon = Image.new("RGBA", (50, 50), color="blue")
        icon.save(icon_path)

        result_image = add_icon_to_image(image, str(icon_path))
        assert result_image is not None
        assert isinstance(result_image, Image.Image)


class TestAddFrameToImage:

    def test_add_simple_frame_to_image(self):
        image = Image.new("RGBA", (200, 200), color="white")
        result_image = add_frame_to_image(image, frame_type="simple")
        assert result_image is not None
        assert isinstance(result_image, Image.Image)

    def test_add_rounded_frame_to_image(self):
        image = Image.new("RGBA", (200, 200), color="white")
        result_image = add_frame_to_image(image, frame_type="rounded")
        assert result_image is not None
        assert isinstance(result_image, Image.Image)
