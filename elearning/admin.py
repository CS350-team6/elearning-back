from django.contrib import admin
from .models.user import UserInfo, JWTToken
from .models.video import Video

admin.site.register(UserInfo)
admin.site.register(JWTToken)
admin.site.register(Video)