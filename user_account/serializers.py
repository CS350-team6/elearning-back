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

class UserJWTSerializer(serializers.Serializer):
    ##userId = serializers.EmailField(required=True)
    jwtToken = serializers.CharField(required=True)

    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        ##instance.userId = validated_data.get('userId', instance.userId)
        instance.jwtToken = validated_data.get('jwtToken', instance.jwtToken)
        instance.save()
        return instance
    
    class Meta:
        model = User
        fields = '__all__'
        # fields = ['id', 'username']

class UserPwChangeSerializer(serializers.Serializer):
    ##userId = serializers.EmailField(required=True)
    userId = serializers.EmailField(required=True)
    userPw = serializers.CharField(required=True)
    newPw = serializers.CharField(required=True)

    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        ##instance.userId = validated_data.get('userId', instance.userId)
        instance.userId = validated_data.get('userId', instance.userId)
        instance.userPw = validated_data.get('userPw', instance.userPw)
        instance.newPw = validated_data.get('newPw', instance.newPw)
        instance.save()
        return instance
    
    class Meta:
        model = User
        fields = '__all__'
        # fields = ['id', 'username']

class UserPwResetSerializer(serializers.Serializer):
    ##userId = serializers.EmailField(required=True)
    userId = serializers.EmailField(required=True)

    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        ##instance.userId = validated_data.get('userId', instance.userId)
        instance.userId = validated_data.get('userId', instance.userId)
        instance.save()
        return instance
    
    class Meta:
        model = User
        fields = '__all__'
        # fields = ['id', 'username']
