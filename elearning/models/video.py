from django.db import models
from ..models.lecture import Lecture

class Video(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=100, default='title')
    description = models.TextField(default='description')
    thumbnail = models.FileField()
    video_file = models.FileField()
    play_count = models.IntegerField(default=0)
    understood_count = models.IntegerField(default=0)
    notunderstood_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        verbose_name_plural = 'videos'