from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

def get_default_user():
    return None

class JWTToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_valid(self):
        return not self.is_expired()

    def is_expired(self):
        return self.created_at < timezone.now() - timedelta(days=1)
    
    def __str__(self):
        return f"JWT({self.user}) - {self.token}"

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    jwt_token = models.ForeignKey(JWTToken, on_delete=models.SET_NULL, null=True)
    nickname = models.CharField(max_length=50)
    validation_code = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f"{self.user_id} - {self.nickname}"

    #def was_published_recently(self):
    #    return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

