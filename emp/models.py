from django.db import models

# Create your models here.

from django.db import models
import datetime

class Employee(models.Model):
    work_status=[
        ('intime','In time'),
        ('delayed','Delayed'),
    ]
    name = models.CharField(max_length=100)
    emp_id = models.CharField(max_length=50)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10,choices=work_status)
    total_hours_worked = models.FloatField()
    overtime_status = models.CharField(max_length=50)