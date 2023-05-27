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

class Student(models.Model):
    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    # Add additional fields specific to the Student table
    student_id = models.CharField(max_length=20)
    major = models.CharField(max_length=100)

    def __str__(self):
        return self.user.nickname


class Instructor(models.Model):
    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    # Add additional fields specific to the Instructor table
    instructor_id = models.CharField(max_length=20)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.user.nickname