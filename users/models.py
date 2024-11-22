from django.contrib.auth.models import AbstractUser
from django.db import models
import random

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

    def create_verify_code(self):
        code = random.randint(10000,99999)
        UserConfirmation.objects.create(
            user=self,
            code=code
        )
        return code
    

class UserConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation')
    code = models.CharField(max_length=5)
    is_confirmed = models.BooleanField(default=False)


    def __str__(self):
        return f"Confirmation for {self.user.username}"



from django.db import models
from django.conf import settings

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses')

    def str(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='groups_groups')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='groups_students')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_groups_by_salohiddn')

    def str(self):
        return f"{self.name} ({self.course.name})"
    

