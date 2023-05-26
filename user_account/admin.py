from django.contrib import admin
from .models import UserInfo, JWTToken
# Register your models here.
admin.site.register(UserInfo)
admin.site.register(JWTToken)