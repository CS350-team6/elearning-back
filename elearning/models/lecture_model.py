from django.db import models

class Lecture(models.Model):
    title = models.CharField(max_length=100, default='lecture_title')
    description = models.TextField(default='lecture_description')
    instructor = models.CharField(max_length=100, default='instructor')
    year = models.CharField(max_length=4, default='2023')
    semester = models.CharField(max_length=10, default='spring')
    thumbnail = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return f"{self.title}"
    class Meta:
        verbose_name_plural = 'lectures'

class Video(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=100, default='video_title')
    description = models.TextField(default='video_description')
    thumbnail = models.FileField(blank=True)
    video_file = models.FileField(blank=True)
    play_count = models.IntegerField(default=0)
    understood_count = models.IntegerField(default=0)
    notunderstood_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
 
    class Meta:
        verbose_name_plural = 'videos'