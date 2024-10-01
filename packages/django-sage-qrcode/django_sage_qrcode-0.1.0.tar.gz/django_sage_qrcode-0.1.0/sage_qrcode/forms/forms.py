from django import forms
from sage_qrcode.models import (
    VCardQRCode,
    WifiQRCode,
    MediaUrl,
    EPCQRCode,
    TikTokQRCode,
    BitcoinQRCode,
    XQRCode,
)

import uuid
import os


class VCardQRCodeForm(forms.ModelForm):
    class Meta:
        model = VCardQRCode
        fields = ["full_name", "display_name", "email", "phone", "url", "custom_gif"]

    def save(self, commit=True):
        """Custom save method to handle the storage of a custom GIF file
        associated with a VCard QR Code."""
        instance = super().save(commit=False)
        custom_gif = self.cleaned_data.get("custom_gif", None)
        if custom_gif:
            unique_id = uuid.uuid4().hex
            file_name = f"{unique_id}_{custom_gif.name}"
            upload_path = os.path.join("uploads", unique_id)
            os.makedirs(upload_path, exist_ok=True)
            file_path = os.path.join(upload_path, file_name)
            with open(file_path, "wb+") as destination:
                for chunk in custom_gif.chunks():
                    destination.write(chunk)
            instance.custom_gif_path = file_path

        if commit:
            instance.save()
        return instance


class WiFiQRCodeForm(forms.ModelForm):
    class Meta:
        model = WifiQRCode
        fields = ["ssid", "password", "security", "custom_gif"]

    def save(self, commit=True):
        """Custom save method to handle the storage of a custom GIF file
        associated with a WiFi QR Code."""
        instance = super().save(commit=False)
        custom_gif = self.cleaned_data.get("custom_gif", None)

        if custom_gif:
            unique_id = uuid.uuid4().hex
            file_name = f"{unique_id}_{custom_gif.name}"
            upload_path = os.path.join("uploads", unique_id)
            os.makedirs(upload_path, exist_ok=True)
            file_path = os.path.join(upload_path, file_name)
            with open(file_path, "wb+") as destination:
                for chunk in custom_gif.chunks():
                    destination.write(chunk)
            instance.custom_gif_path = file_path
        if commit:
            instance.save()
        return instance


class TikTokForm(forms.ModelForm):
    """A form for creating TikTok QR Codes."""

    class Meta:
        model = TikTokQRCode
        fields = ["url", "custom_gif", "color", "second_color", "third_color"]


class XForm(forms.ModelForm):
    """A form for creating X QR Codes."""

    class Meta:
        model = XQRCode
        fields = ["url", "custom_gif", "color", "second_color", "third_color"]


class MediaUrlForm(forms.ModelForm):
    class Meta:
        model = MediaUrl
        fields = ["url", "custom_gif"]

    def save(self, commit=True):
        """Custom save method to handle the storage of a custom GIF file
        associated with a Media URL QR Code."""
        instance = super().save(commit=False)
        custom_gif = self.cleaned_data.get("custom_gif", None)
        if custom_gif:
            unique_id = uuid.uuid4().hex
            file_name = f"{unique_id}_{custom_gif.name}"
            upload_path = os.path.join("uploads", unique_id)
            os.makedirs(upload_path, exist_ok=True)
            file_path = os.path.join(upload_path, file_name)
            with open(file_path, "wb+") as destination:
                for chunk in custom_gif.chunks():
                    destination.write(chunk)
            instance.custom_gif_path = file_path
        if commit:
            instance.save()
        return instance


class EPCQRCodeForm(forms.ModelForm):
    class Meta:
        model = EPCQRCode
        fields = ["name", "iban", "amount", "text", "custom_gif"]

    def save(self, commit=True):
        """Custom save method to handle the storage of a custom GIF file
        associated with an EPC QR Code."""
        instance = super().save(commit=False)
        custom_gif = self.cleaned_data.get("custom_gif", None)
        if custom_gif:
            unique_id = uuid.uuid4().hex
            file_name = f"{unique_id}_{custom_gif.name}"
            upload_path = os.path.join("uploads", unique_id)
            os.makedirs(upload_path, exist_ok=True)
            file_path = os.path.join(upload_path, file_name)
            with open(file_path, "wb+") as destination:
                for chunk in custom_gif.chunks():
                    destination.write(chunk)
            instance.custom_gif_path = file_path
        if commit:
            instance.save()
        return instance


class BitForm(forms.ModelForm):
    class Meta:
        model = BitcoinQRCode
        fields = [
            "bitcoin_address",
            "amount",
            "label",
            "message",
            "second_color",
            "color",
            "third_color",
        ]

    def save(self, commit=True):
        """Custom save method to handle the storage of a custom GIF file
        associated with a Bitcoin QR Code."""
        instance = super().save(commit=False)
        custom_gif = self.cleaned_data.get("custom_gif", None)
        if custom_gif:
            unique_id = uuid.uuid4().hex
            file_name = f"{unique_id}_{custom_gif.name}"
            upload_path = os.path.join("uploads", unique_id)
            os.makedirs(upload_path, exist_ok=True)
            file_path = os.path.join(upload_path, file_name)
            with open(file_path, "wb+") as destination:
                for chunk in custom_gif.chunks():
                    destination.write(chunk)
            instance.custom_gif_path = file_path
        if commit:
            instance.save()
        return instance
