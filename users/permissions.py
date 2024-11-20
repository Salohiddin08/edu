from rest_framework.permissions import BasePermission

class IsAdminOrTeacher(BasePermission):
    def has_permission(self, request, view):
        # Faqat admin yoki teacher boshqara oladi
        return request.user.role in ['admin', 'teacher']

    def has_object_permission(self, request, view, obj):
        # Faqat admin yoki teacher o'ziga tegishli kurs/guruhni boshqara oladi
        return request.user.role in ['admin', 'teacher'] and obj.teacher == request.user