from django.db import models
from django.contrib.auth.models import User

class Lecture(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lectures', blank=True, null=True)
    title = models.CharField(max_length=100, default='title')
    description = models.TextField(default='description')
    year = models.CharField(max_length=4, default='2023')
    semester = models.CharField(max_length=10, default='spring')
    thumbnail = models.FileField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'lectures'

class Video(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='videos', blank=True, null=True)
    title = models.CharField(max_length=100, default='video title')
    description = models.TextField(default='video description')
    thumbnail = models.FileField(blank=True)
    video_file = models.FileField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
 
    class Meta:
        verbose_name_plural = 'videos'

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    content = models.TextField(default='comment content')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlists', blank=True, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='watchlists', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', blank=True, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Understand(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='understands', blank=True, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='understands', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NotUnderstand(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notunderstands', blank=True, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='notunderstands', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class VideoPlay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videoplays', blank=True, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='videoplays', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)