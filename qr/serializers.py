from rest_framework import serializers

from qr.models import QRCode, SaveQRCode

class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = ['id', 'content', 'image', 'created_at', 'user']
        read_only_fields = ['id', 'image', 'created_at', 'user']


class SaveQRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaveQRCode
        fields = ['id', 'qrcode', 'user', 'name']
        read_only_fields = ['id', 'user']