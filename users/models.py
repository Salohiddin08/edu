from django.contrib.auth.models import AbstractUser
from django.db import models
import random
from rest_framework_simplejwt.tokens import RefreshToken
class User(AbstractUser):
    # User rollari uchun choices
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    
    # User rolini belgilash uchun maydon
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student',  # Default 'student' rolini belgilaymiz
    )

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }




    def create_verify_code(self):
        code = random.randint(10000,99999)
        UserConfirmation.objects.create(
            user=self,
            code=code
        )
        return code
    


from datetime import timedelta
from django.utils import timezone

class UserConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation')
    code = models.CharField(max_length=5)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()


    def __str__(self):
        return f"Confirmation for {self.user.code}"
    
    def save(self, *args, **kwargs):
        self.expires_at = timezone.now() + timedelta(minutes=5)
        super(UserConfirmation, self).save(*args, **kwargs)



from django.db import models
from django.conf import settings

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses')

    def str(self):
        return self.name

from django.db import models
from django.conf import settings
from datetime import time

class Group(models.Model):
    
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='groups_groups')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='groups_students')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_groups_by_salohiddn')
    study_time = models.TimeField(default=time(9, 0))
    days_of_week = models.CharField(max_length=50, default='Mon,Wed,Fri')

    def __str__(self):
        return self.name


    def str(self):
        return f"{self.name} ({self.course.name})"
    

