from django.urls import path, include

from rest_framework.routers import DefaultRouter
from qr.views import QRCodeViewSet

router = DefaultRouter()
router.register(r'qrcode', QRCodeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]