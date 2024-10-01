import io
import time
import zipfile
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.contrib import messages

from sage_qrcode.service import (
    ContactQRCode,
    SocialMediaQRCode,
    PaymentQRCode,
    QRCodeBase,
    BarcodeProxy,
)

from sage_qrcode.models import (
    VCardQRCode,
    WifiQRCode,
    TikTokQRCode,
    TelegramQRCode,
    InstagramQRCode,
    SnapchatQRCode,
    SkypeQRCode,
    XQRCode,
    WhatsAppQRCode,
    FacebookQRCode,
    EPCQRCode,
    MediaUrl,
    LinkedInQRCode,
    BitcoinQRCode,
    BarcodeText,
    BarcodeUrl,
)


def generate_qr_code(obj: QRCodeBase) -> bytes:
    """Generates a QR code image based on the type of object passed.

    Args:
        obj (QRCodeBase): An instance of a subclass of QRCodeBase containing data to generate a QR code.

    Returns:
        bytes: The generated QR code image in bytes.

    """
    proxy = QRCodeBase()
    custom_gif_path = obj.custom_gif_path if obj.custom_gif else None
    obj.size = obj.size or 10
    if not obj.second_color:
        obj.second_color = "#FFFFFF"
    if not obj.third_color:
        obj.third_color = "#000000"

    media_classes = (
        TikTokQRCode,
        TelegramQRCode,
        InstagramQRCode,
        SnapchatQRCode,
        SkypeQRCode,
        WhatsAppQRCode,
        FacebookQRCode,
        LinkedInQRCode,
        XQRCode,
    )

    if isinstance(obj, VCardQRCode):
        contact_proxy = ContactQRCode()
        contact_proxy.generate_vcard_qr_code(
            name=obj.full_name,
            displayname=obj.display_name,
            email=obj.email,
            phone=obj.phone,
            url=obj.url,
            address=obj.address,
            org=obj.org,
            custom=custom_gif_path,
            color=obj.color,
            size=obj.size,
            color2=obj.second_color,
            color3=obj.third_color,
        )
        proxy.qr_image = contact_proxy.qr_image
    elif isinstance(obj, WifiQRCode):
        contact_proxy = ContactQRCode()
        contact_proxy.generate_wifi_qr_code(
            ssid=obj.ssid,
            password=obj.password,
            security_type=obj.security,
            custom=custom_gif_path,
            color=obj.color,
            color2=obj.second_color,
            color3=obj.third_color,
            size=obj.size,
        )
        proxy.qr_image = contact_proxy.qr_image
    elif isinstance(obj, media_classes):
        social_proxy = SocialMediaQRCode()
        social_proxy.create_social_media_url(
            url=obj.url,
            color=obj.color,
            size=obj.size,
            color2=obj.second_color,
            color3=obj.third_color,
        )
        proxy.qr_image = social_proxy.qr_image
    elif isinstance(obj, MediaUrl):
        social_proxy = SocialMediaQRCode()
        social_proxy.create_url(
            playlist_url=obj.url,
            custom=custom_gif_path,
            color=obj.color,
            size=obj.size,
            color2=obj.second_color,
            color3=obj.third_color,
        )
        proxy.qr_image = social_proxy.qr_image
    elif isinstance(obj, EPCQRCode):
        payment_proxy = PaymentQRCode()
        payment_proxy.generate_epc_qr_code(
            name=obj.name,
            iban=obj.iban,
            color=obj.color,
            size=obj.size,
            amount=obj.amount,
            text=obj.text,
            custom=custom_gif_path,
            color2=obj.second_color,
            color3=obj.third_color,
        )
        proxy.qr_image = payment_proxy.qr_image
    elif isinstance(obj, BitcoinQRCode):
        payment_proxy = PaymentQRCode()
        payment_proxy.generate_bitcoin_qr_code(
            address=obj.bitcoin_address,
            amount=obj.amount,
            label=obj.label,
            message=obj.message,
            color2=obj.second_color,
            color3=obj.third_color,
        )
        proxy.qr_image = payment_proxy.qr_image
    return proxy.show_qr_code(save=False)


def save_qr_code_image(obj: QRCodeBase, qr_image: bytes) -> None:
    """Saves the generated QR code image to the database.

    Args:
        obj (QRCodeBase): An instance of a subclass of QRCodeBase.
        qr_image (bytes): The generated QR code image in bytes.

    """
    buffer = io.BytesIO()
    qr_image.save(buffer, format="PNG")
    obj.qr_code_image.save(
        f"{obj.pk}_qr.png", ContentFile(buffer.getvalue()), save=False
    )


def handle_qr_code(request: HttpResponse, queryset) -> HttpResponse:
    """Handles the HTTP request to download QR codes.

    Args:
        request (HttpResponse): The HTTP request object.
        queryset: A queryset containing the objects to be downloaded.

    Returns:
        HttpResponse: The HTTP response containing the QR code image(s).

    """
    start_time = time.time()

    if queryset.count() == 0:
        return HttpResponse("Please select at least one QR code to download.")
    elif queryset.count() == 1:
        obj = queryset.first()
        response = HttpResponse(content_type="image/png")
        response["Content-Disposition"] = f"attachment; filename={obj.pk}_qr.png"
        with obj.qr_code_image.open("rb") as img_file:
            response.write(img_file.read())
        return response
    else:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for obj in queryset:
                with obj.qr_code_image.open("rb") as img_file:
                    zip_file.writestr(f"{obj.pk}_qr.png", img_file.read())

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type="application/zip")
        response["Content-Disposition"] = 'attachment; filename="Qrcodes.zip"'

        end_time = time.time()
        runtime = end_time - start_time
        messages.success(
            request,
            "Successfully prepared download for {} QR codes in {:.2f} seconds.".format(
                queryset.count(), runtime
            ),
        )
        return response


def download_qr_code(self, request, queryset):
    response = handle_qr_code(request, queryset)
    if isinstance(response, HttpResponse):
        self.message_user(request, "Please select exactly one QR code to download.")
    return response


def generate_barcode_image(obj: BarcodeProxy) -> bytes:
    """Generates a barcode image based on the type of object passed.

    Args:
        obj (BarcodeProxy): An instance of a subclass of BarcodeProxy containing data to generate a barcode.

    Returns:
        bytes: The generated barcode image in bytes.

    """
    proxy = BarcodeProxy()
    if not obj.color:
        obj.color = "black"
    if not obj.second_color:
        obj.second_color = "white"
    if isinstance(obj, BarcodeUrl):
        proxy.create_url(url=obj.url, bar_color=obj.color, bg_color=obj.second_color)
    elif isinstance(obj, BarcodeText):
        proxy.create_text_barcode(
            text=obj.body, bar_color=obj.color, bg_color=obj.second_color
        )
    return proxy.show_barcode(save=False)


def save_barcode_image(obj: BarcodeProxy, barcode_image: bytes) -> None:
    """Saves the generated barcode image to the database.

    Args:
        obj (BarcodeProxy): An instance of a subclass of BarcodeProxy.
        barcode_image (bytes): The generated barcode image in bytes.

    """
    buffer = io.BytesIO()
    barcode_image.save(buffer, format="PNG")
    obj.bar_code_image.save(
        f"{obj.pk}_barcode.png", ContentFile(buffer.getvalue()), save=False
    )


def download_barcode(request: HttpResponse, queryset) -> HttpResponse:
    """Handles the HTTP request to download barcodes.

    Args:
        request (HttpResponse): The HTTP request object.
        queryset: A queryset containing the objects to be downloaded.

    Returns:
        HttpResponse: The HTTP response containing the barcode image(s).

    """
    if queryset.count() == 0:
        return HttpResponse("Please select at least one barcode to download.")
    elif queryset.count() == 1:
        obj = queryset.first()
        response = HttpResponse(content_type="image/png")
        response["Content-Disposition"] = f"attachment; filename={obj.pk}_barcode.png"
        with obj.bar_code_image.open("rb") as img_file:
            response.write(img_file.read())
        return response
    else:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for obj in queryset:
                with obj.bar_code_image.open("rb") as img_file:
                    zip_file.writestr(f"{obj.pk}_barcode.png", img_file.read())

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type="application/zip")
        response["Content-Disposition"] = 'attachment; filename="Barcodes.zip"'

        messages.success(
            request,
            "Successfully prepared download for {} barcodes.".format(queryset.count()),
        )
        return response
