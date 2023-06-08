from rest_framework import viewsets
from rest_framework.decorators import action
from ..models.user_info_model import UserInfo
from ..serializers.user_info import UserInfoSerializer

class UserInfoViewset(viewsets.ModelViewset):
    serializer_class = UserInfoSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = UserInfo.objects.all()
    