from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import User, UserConfirmation
from.send_phone_code import send_phone_code
from .serializers import UserSerializer, LoginSerializer, UserListSerializer
from rest_framework import generics


# Register View - Ro'yxatdan o'tish 
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Autentifikatsiya talab qilinmasin

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = RefreshToken.for_user(user)
            return Response({
                'message': 'User created successfully!',
                'access_token': str(token.access_token),
                'refresh_token': str(token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login View - Kirish
class LoginView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        username = request.data.get('username', None)
        email = request.data.get('email', None)
        phone = request.data.get('phone', None)
        password = request.data.get('password', None)
        if not (username or email or phone):
            return Response({'error': 'Username, email, or phone is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Foydalanuvchini tekshiris
        user = None
        if username:
            user = authenticate(username=username, password=password)
        elif email:
            try:
                user = authenticate(username=User.objects.get(email=email).username, password=password)
            except User.DoesNotExist:
                return Response({'error': 'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
        elif phone:
            try:
                user = authenticate(username=User.objects.get(phone=phone).username, password=password)
            except User.DoesNotExist:
                return Response({'error': 'No user found with this phone number.'}, status=status.HTTP_400_BAD_REQUEST)

        # Agar foydalanuvchi topilsa
        if user is not None:
            # JWT token yaratish
            token = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful!',
                'access_token': str(token.access_token),
                'refresh_token': str(token),
            })
        
        # Agar foydalanuvchi topilmasa
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


# Token Refresh View - Tokenni yangilash
class TokenRefreshView(APIView):
    permission_classes = [AllowAny]  # Avtorizatsiya talab qilinmaydi

    def post(self, request):
        refresh_token = request.data.get('refresh_token', None)
        if refresh_token is None:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)
            return Response({'access_token': new_access_token})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# User List View - Foydalanuvchilarni ro'yxatini olish va role bo'yicha filtrlash
class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        role_filter = self.request.query_params.get('role', None)
        if role_filter:
            queryset = queryset.filter(role=role_filter)  # Role bo'yicha filtrlash
        return queryset
from rest_framework import generics
from .models import User
from .serializers import UserListSerializer
from .filters import UserFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions

class UserListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    filter_backends = [DjangoFilterBackend]  # Filtrlar backendini qo'shish
    filterset_class = UserFilter  # Filtrlash uchun filterset_class ni belgilash



from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course, Group
from .serializers import CourseSerializer, GroupSerializer
from .permissions import IsAdminOrTeacher

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]

    def perform_create(self, serializer):
        # Teacher kurs yaratadi
        serializer.save(teacher=self.request.user)
from rest_framework import viewsets
from .models import Group
from .serializers import GroupSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrTeacher

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]



    def perform_create(self, serializer):
        # Admin yoki teacher guruh yaratadi
        serializer.save(created_by=self.request.user)

from django.utils import timezone
from rest_framework.exceptions import  ValidationError
class UserConfirmationCodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        user = request.user
        code = request.data.get('code')
        self.check_verify(user=user, code=code)
        return Response(data={
            'message': 'User confirmed successfully!',
            'access_token' : user.token()['access'],
            'refresh_token' : user.token()['refresh'],

        }, status=status.HTTP_200_OK)

    @staticmethod
    def check_verify(user, code):
        verifies = UserConfirmation.objects.filter(user=user, code=code, is_confirmed=False, expires_at__gte=timezone.now())
        if not verifies.exists():
            data = {
                'error': 'Invalid confirmation code or expiration'

            }
            raise ValidationError(data)
        user_confirm = verifies.first()
        user_confirm.is_confirmed = True
        user_confirm.save()
        return True
    

class GetNewCode(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        self.check_new_verify(user=user)
        code = user.create_verify_code()
        latest_code = user.verify_codes.order_by('-created_at').first()
        user.verify_codes.exclude(id=latest_code.id).delete()
        send_phone_code(code=code)
        return Response(data={
            'message':"Code returned sent",
            'access_token':user.token()['access'],
            'refresh_token':user.token()['refresh'],

        },status=status.HTTP_201_CREATED)
    @staticmethod
    def check_new_verify(user):
        verifies = UserConfirmation.objects.filter(expires_at__gte=timezone.now(), is_confirmed=False, user=user)
        print(verifies)
        if verifies.exists():
            raise ValidationError({
                'error': 'User already has a pending confirmation.'
            })
        return True



        

        # user_confirm = UserConfirmation.objects.filter(user=user, code=code, is_confirmed=False).first()
        # if user_confirm:
        #     user_confirm.is_confirmed = True
        #     user_confirm.save()
        #     return Response({'message': 'User confirmed successfully!'}, status=status.HTTP_200_OK)
        # return Response(data={'message': 'User unconfirmed successfully!'}, status=status.HTTP_400_BAD_REQUEST)