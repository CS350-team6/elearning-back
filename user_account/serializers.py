from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserInfo

class UserLoginSerializer(serializers.Serializer):
    # userinfo = serializers.PrimaryKeyRelatedField(many=False, queryset=UserInfo.objects.all()
    userId = serializers.EmailField(required=True)
    userPw = serializers.CharField(required=True)

    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.userId = validated_data.get('userId', instance.userId)
        instance.userPw = validated_data.get('userPw', instance.userPw)
        instance.save()
        return instance
    
    class Meta:
        model = User
        fields = '__all__'
        # fields = ['id', 'username']

class UserInfoSerializer(serializers.Serializer):
    class Meta:
        model = UserInfo
        fields = '__all__'

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = '__all__'

