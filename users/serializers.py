# api/serializers.py

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # Userni yaratish
        return user
# api/serializers.py

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
# api/serializers.py

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']


from rest_framework import serializers
from .models import Course, Group
from users.models import User  # Foydalanuvchi modeli

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'teacher']

class GroupSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='student'), many=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'course', 'students', 'created_by']
