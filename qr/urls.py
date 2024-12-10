from django.urls import path, include

from rest_framework.routers import DefaultRouter
from qr.views import QRCodeViewSet, SaveQRCodeViewSet

router = DefaultRouter()
router.register(r'qrcode', QRCodeViewSet)
router.register(r'save', SaveQRCodeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]