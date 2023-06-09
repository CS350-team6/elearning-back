from django.contrib import admin
from .models import user_info_model, lecture_model
from django.contrib.auth.models import User

admin.site.register(user_info_model.JWTToken)
admin.site.register(lecture_model.Video)
admin.site.register(lecture_model.Lecture)