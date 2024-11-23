from rest_framework.routers import DefaultRouter
from django.urls import path, include

# from .views import StudentViewSet

# router = DefaultRouter()

# router.register(r'', StudentViewSet, basename='student')

# urlpatterns = [
#     path('', include(router.urls)),
# ]

from .views import StudentAPIView, StudentDetailAPIView

urlpatterns = [
    path('students/', StudentAPIView.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentDetailAPIView.as_view(), name='student-detail'),
]