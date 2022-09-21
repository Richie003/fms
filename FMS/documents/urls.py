from django.urls import path
from . import views
import secrets

random = secrets.token_urlsafe()

urlpatterns = [
    path('', views.index, name='home'),
    path('<str:name>/', views.folderItems, name='folder_files'),
    path('delete/<int:pk>/', views.remove_folder, name='delete_folder'),
    path('delete/files/', views.remove_all, name='delete_all'),
    path('delete/file/<int:pk>/', views.remove_file, name='delete_file'),
    path('download/<str:file_name>/', views.download, name='download_file'),
    # Url for getting folders belonging to a user
    path('user_folder/', views.get_folders, name='folders')
]
