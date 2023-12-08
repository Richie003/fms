from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views
import secrets

random = secrets.token_urlsafe()

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path(f'logout/', views.log_out, name='log_out'),
]
