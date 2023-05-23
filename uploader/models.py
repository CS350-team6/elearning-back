from django.db import models
 
class Video(models.Model):
    title = models.CharField(max_length=30)
    video_file = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        verbose_name_plural = 'videos'