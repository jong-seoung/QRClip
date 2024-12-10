from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from qr.serializers import QRCodeSerializer
from qr.models import QRCode
from core.mixins import CreateModelMixin, MappingViewSetMixin

class QRCodeViewSet(MappingViewSetMixin, GenericViewSet, CreateModelMixin):
    serializer_class = QRCodeSerializer
    serializer_action_map = {
        "create": QRCodeSerializer,
    }
    queryset = QRCode.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)