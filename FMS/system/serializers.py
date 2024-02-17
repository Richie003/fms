from rest_framework import serializers
from accounts.models import User
from documents.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['email', 'username', 'tel', 'verified', 'password']


class FolderSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Folder
        fields = [
            'user',
            'folder'
        ]

class FileSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = FileData
        fields = [
            'user',
            'file'
        ]