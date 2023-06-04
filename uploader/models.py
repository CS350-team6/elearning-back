from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=100, default='title')
    description = models.TextField(default='description')
    year = models.CharField(max_length=4, default='2023')
    semester = models.CharField(max_length=10, default='spring')
    lecture = models.CharField(max_length=100, default='lecture')
    instructor = models.CharField(max_length=100, default='instructor')
    thumbnail = models.FileField()
    play_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    video_file = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        verbose_name_plural = 'videos'