from django.contrib import admin
from .models import Video, Lecture, Comment
admin.site.register(Lecture)
admin.site.register(Video)
admin.site.register(Comment)