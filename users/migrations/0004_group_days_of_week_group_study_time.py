# Generated by Django 5.1.3 on 2024-12-05 04:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userconfirmation_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='days_of_week',
            field=models.CharField(default='Mon,Wed,Fri', max_length=50),
        ),
        migrations.AddField(
            model_name='group',
            name='study_time',
            field=models.TimeField(default=datetime.time(9, 0)),
        ),
    ]