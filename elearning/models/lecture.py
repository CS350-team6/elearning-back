from django.db import models

class Lecture(models.Model):
    title = models.CharField(max_length=100, default='title')
    description = models.TextField(default='description')
    instructor = models.CharField(max_length=100, default='instructor')
    year = models.CharField(max_length=4, default='2023')
    semester = models.CharField(max_length=10, default='spring')
    thumbnail = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        verbose_name_plural = 'lectures'