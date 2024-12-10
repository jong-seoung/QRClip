from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from io import BytesIO

import qrcode

from core.models import TimeStampModel

class QRCode(TimeStampModel):
    content = models.TextField()
    image = models.ImageField(upload_to='qrcodes/', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='qrcodes')

    def save(self, *args, **kwargs):
        qr_image = qrcode.make(self.content)
        buffer = BytesIO()
        qr_image.save(buffer, format="WEBP")

        self.image.save(f"qr.webp", ContentFile(buffer.getvalue()), save=False)
        super().save(*args, **kwargs)
        

class SaveQRCode(TimeStampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_qrcodes')
    qrcode = models.ForeignKey(QRCode, on_delete=models.CASCADE, related_name='saved_by_users')
    name = models.CharField(max_length=100)

