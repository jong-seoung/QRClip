from rest_framework import serializers

from qr.models import QRCode

class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = ['id', 'content', 'image', 'created_at', 'user']
        read_only_fields = ['id', 'image', 'created_at', 'user']
