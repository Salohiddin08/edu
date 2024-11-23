from django.db import models


class Students(models.Model):
    name = models.CharField(max_length=100)
    body = models.TextField()
    
    def __str__(self):
        return f'{self.name} {self.body}'