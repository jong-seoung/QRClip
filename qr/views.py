from django.db.models import Q

from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from qr.serializers import QRCodeSerializer, SaveQRCodeSerializer
from qr.models import QRCode, SaveQRCode
from core.mixins import MappingViewSetMixin, CreateModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin

class QRCodeViewSet(MappingViewSetMixin, GenericViewSet, CreateModelMixin):
    serializer_class = QRCodeSerializer
    serializer_action_map = {
        "create": QRCodeSerializer,
    }
    queryset = QRCode.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        content = request.data.get("content")

        existing_qr = QRCode.objects.filter(Q(content=content)).first()

        if existing_qr:
            serializer = self.get_serializer(existing_qr)
            return Response(serializer.data, status=status.HTTP_200_OK)


class SaveQRCodeViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin):
    serializer_class = SaveQRCodeSerializer
    queryset = SaveQRCode.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        self.queryset = SaveQRCode.objects.filter(user=request.user)
        return super().list(request, *args, **kwargs)