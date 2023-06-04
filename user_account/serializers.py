from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserInfo

class UserInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserInfo
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # userinfo = serializers.PrimaryKeyRelatedField(many=False, queryset=UserInfo.objects.all())

    class Meta:
        model = User
        fields = '__all__'
        # fields = ['id', 'username']