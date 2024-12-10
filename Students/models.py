from django.db import models

class Students(models.Model):
    name = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self):
        return f'{self.name} {self.body}'

class Attendance(models.Model):
    student = models.ForeignKey(Students, related_name='attendances', on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField()

    def __str__(self):
        return f'{self.student.name} - {self.date} - {"Present" if self.status else "Absent"}'

class Payment(models.Model):
    student = models.ForeignKey(Students, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f'{self.student.name} - {self.amount} - {self.date}'
