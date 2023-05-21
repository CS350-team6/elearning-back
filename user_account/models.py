from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class UserInfo(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user_id} - {self.nickname}"

    #def was_published_recently(self):
    #    return self.pub_date >= timezone.now() - datetime.timedelta(days=1)