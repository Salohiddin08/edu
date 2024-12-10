# from rest_framework.routers import DefaultRouter
# from django.urls import path, include

# # from .views import StudentViewSet

# # router = DefaultRouter()

# # router.register(r'', StudentViewSet, basename='student')

# # urlpatterns = [
# #     path('', include(router.urls)),
# # ]

# from .views import StudentAPIView, StudentDetailAPIView

# urlpatterns = [
#     path('students/', StudentAPIView.as_view(), name='student-list'),
#     path('students/<int:pk>/', StudentDetailAPIView.as_view(), name='student-detail'),
# ]

from django.urls import path
from .views import StudentAPIView, StudentDetailAPIView, MarkAttendanceAPIView, MakePaymentAPIView

urlpatterns = [
    path('', StudentAPIView.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentDetailAPIView.as_view(), name='student-detail'),
    path('students/<int:student_id>/attendance/', MarkAttendanceAPIView.as_view(), name='mark-attendance'),
    path('students/<int:student_id>/payment/', MakePaymentAPIView.as_view(), name='make-payment'),
]
