from rest_framework import viewsets
from fms_app.serializers import FileSerializer
from fms_app.models import File

# Create your views here.


class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    queryset = File.objects.all()
