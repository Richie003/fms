"""system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/user011/', admin.site.urls),
    path('', include('documents.urls')),
    path('accounts/', include('accounts.urls')),
    # APIs for NlightR
    path('api/login/', views.login),
    path('api/sign_up/', views.sign_up),
    path('api/validate_username/', views.validate_username),
    path('api/test_token/', views.test_token),
    path('api/createfolder/', views.createFolder),
    path('api/upload-file/', views.uploadFile), #uploadFile
    path('api/get-files/', views.getUniqueFiles),
    path('api/execute_download/', views.downloadable),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
