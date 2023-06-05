from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from ..models.video import Video

def get_default_user():
    return None

class JWTToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, related_name="jwt_token", on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return not self.is_expired()
    
    def is_expired(self):
        return self.created_at < timezone.now() - timedelta(days=1)

    def __str__(self):
        return f"{self.token}"

class UserInfo(models.Model):
    user = models.ForeignKey('auth.User', related_name='userinfo', on_delete=models.CASCADE)
    user_role = models.CharField(max_length=20, default="student")
    jwt_token = models.ForeignKey(JWTToken, on_delete=models.SET_NULL, null=True)
    nickname = models.CharField(max_length=50)
    bookmarked_videos = models.ManyToManyField(Video, related_name="bookmarked_users", blank=True)
    understood_videos = models.ManyToManyField(Video, related_name="understood_users", blank=True)
    notunderstood_videos = models.ManyToManyField(Video, related_name="notunderstood_users", blank=True)
    validation_code = models.CharField(max_length=30, null=True)