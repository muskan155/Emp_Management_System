from django.db import models

class Employee(models.Model):
    work_status=[
        ('intime','In time'),
        ('delayed','Delayed'),
    ]
    name = models.CharField(max_length=100)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10,choices=work_status, default='')
    total_hours_worked = models.FloatField(null=True)
    overtime_status = models.CharField(max_length=50, null=False, default='')
