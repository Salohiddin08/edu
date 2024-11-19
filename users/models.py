from django.contrib.auth.models import AbstractUser
from django.db import models

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

    def __str__(self):
        return self.username
