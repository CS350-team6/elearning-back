from django.db import models
from django.contrib.auth.models import User

class Lecture(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=100, default='title')
    description = models.TextField(default='description')
    year = models.CharField(max_length=4, default='2023')
    semester = models.CharField(max_length=10, default='spring')
    lecture = models.CharField(max_length=100, default='lecture')
    thumbnail = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'lectures'

class Video(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=100, default='video title')
    description = models.TextField(default='video description')
    thumbnail = models.FileField(blank=True)
    play_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    video_file = models.FileField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
 
    class Meta:
        verbose_name_plural = 'videos'