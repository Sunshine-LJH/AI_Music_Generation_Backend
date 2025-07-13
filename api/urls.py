# api/urls.py
from django.urls import path
from .views import handle_signin, upload_and_fetch_music


urlpatterns = [
    # path('csrf/', get_csrf_token, name='get-csrf-token'),
    path('signin/', handle_signin, name='signin'),
    path('create/', upload_and_fetch_music, name='create'),
]
