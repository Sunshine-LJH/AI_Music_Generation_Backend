# api/urls.py
from django.urls import path
from .views import handle_signin, create_music, get_csrf_token

urlpatterns = [
    path('csrf/', get_csrf_token, name='get-csrf-token'),
    path('signin/', handle_signin, name='signin'),
    path('create/', create_music, name='create'),
]
