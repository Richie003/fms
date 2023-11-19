from django.urls import path
from . import views
import secrets

random = secrets.token_urlsafe()

urlpatterns = [
 # The code snippet is defining the URL patterns for a Django web application. Each `path` function
 # call represents a URL pattern that maps to a specific view function.
    path('', views.index, name='home'),
    path('folder/<str:name>/', views.folderItems, name='folder_files'),
    path('delete/<int:pk>/', views.remove_folder, name='delete_folder'),
    path('delete/files/', views.remove_all, name='delete_all'),
    path('delete/file/<int:pk>/', views.remove_file, name='delete_file'),
    path('download/<str:file_name>/', views.download, name='download_file'),
    # Url for getting folders belonging to a user
    path('user_folder/', views.get_folders, name='folders'),
    path("sharefile/", views.generate_share_url, name="gen_link"),
    path('surl/<str:access_link>/<str:uidb64>/', views.validate_share_url, name='share_url'),
    path("authorize/<str:access_link>/<str:ID>/", views.grant_access_via_email),
    path("<str:author>/<str:file>/<str:external_id>/", views.third_party_access, name="third_party")
]