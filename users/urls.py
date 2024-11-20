# api/urls.py

from django.urls import path
from .views import RegisterView, LoginView, UserListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile', UserListView.as_view(), name='user_list'),  # Role filtrlash
]

