from django.urls import path
from . import views
import secrets

random = secrets.token_urlsafe()

urlpatterns = [
# The code snippet is defining the URL patterns for a Django web application. Each `path` function
# call represents a URL pattern that maps to a specific view function.
    path('', views.index, name='home'),
    path('folder/<str:name>/', views.folderItems, name='folder_files'),
    path('dropzone_file/', views.dropzone_file, name="dropzone_file"),
    path('delete/<int:pk>/', views.remove_folder, name='delete_folder'),
    # Create sub_folder
    path('subfolder/', views.create_subfolder, name='create_subfolder'),
    path('delete/files/', views.remove_all, name='delete_all'),
    path('delete/file/<str:pk>/', views.remove_file, name='delete_file'),
    path('download/<str:file_name>/<str:folder>', views.download, name='download_file'),
    # Url for getting folders belonging to a user
    path('user_folder/', views.get_folders, name='folders'),
    path("sharefile/", views.generate_share_url, name="gen_link"),
    path('surl/<str:access_link>/<str:uidb64>/', views.validate_share_url, name='share_url'),
    path("authorize/<str:access_link>/<str:ID>/", views.grant_access_via_email),
    path("<str:author>/<str:folder>/<str:file>/<str:external_id>/", views.third_party_access, name="third_party"),
    # Search Files URL path
    path('search/', views.searchFunc, name='search'),
    # Terminal/shell url path
    path('termi-shell/', views.terminal_shell, name="termi_shell"),
    path('terminal/query/', views.list_directory),
    path('enter_dir/', views.enter_dir),
    # Send random email
    path('send_mails/', views.send_random_email),
    path('for-Sharon-Echi/', views.love)
]
