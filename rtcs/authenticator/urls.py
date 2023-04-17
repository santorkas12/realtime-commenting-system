from django.urls import path
from .views import LoginService

urlpatterns = [
    path('login/', LoginService.as_view())
]