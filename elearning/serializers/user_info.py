from rest_framework import serializers
from django.contrib.auth.models import User
from ..models.user_info_model import UserInfo

class UserInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserInfo
        fields = '__all__'


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