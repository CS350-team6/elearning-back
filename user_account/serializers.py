from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserInfo

class UserSerializer(serializers.Serializer):
    # userinfo = serializers.PrimaryKeyRelatedField(many=False, queryset=UserInfo.objects.all()
    userId = serializers.EmailField(required=True)
    userPw = serializers.CharField(required=False)
    newPw = serializers.CharField(required=False)
    jwtToken = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = '__all__'
        # fields = ['id', 'username']

class UserInfoSerializer(serializers.Serializer):
    class Meta:
        model = UserInfo
        fields = '__all__'

