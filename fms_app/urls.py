from django.urls import path, include
from rest_framework import routers
from . views import FileViewSet

router = routers.SimpleRouter()
router.register(r"file", FileViewSet, basename="file")

urlpatterns = [
    path("", include(router.urls))
]
