from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import json, jwt
from datetime import datetime, timedelta
from django.conf import settings
from ..models.user import UserInfo, JWTToken
from django.core.mail import send_mail
from rest_framework import viewsets, parsers
from ..serializers.user import UserLoginSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response

def generate_jwt_token(user, user_id):
    # Set the expiration time for the token (e.g., 1 day from now)
    expiration = datetime.utcnow() + timedelta(days=1)

    # Create the payload containing user information
    payload = {
        'user_id': user_id,
        'exp': expiration,
    }

    # Generate the JWT token using the secret key defined in Django settings
    print(payload)
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    JWT = JWTToken.objects.create(
        token = token,
        user = user
    )

    # Return the generated token as a string
    return JWT
    #jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    #serializer_class = UserSerializer
    parser_classes = [parsers.JSONParser]
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) #Raise exception if serializer is not valid (whether there isn't any userId or userPw existing)
        username = serializer.validated_data['userId']
        password = serializer.validated_data['userPw']

        try:
            user = User.objects.create_user(
            username = username,
            password = password,
            )
            user.save()
        except:
            return Response(data=json.dumps({'result': "false", "jwt": "Invaild", "errmsg": "Signup already done with same Id"}), status=400)
        
        print(user)
        print(username)

        JWT = generate_jwt_token(user, username)

        extended_user = UserInfo.objects.create(
            user = user,
            jwt_token = JWT,
            nickname = user.username.split("@")[0]
        )
        extended_user.save()
        return Response(data=json.dumps({'result': "true", "jwt": JWT.token}), status=200)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) #Raise exception if serializer is not valid (whether there isn't any userId or userPw existing)
        username = serializer.validated_data['userId']
        password = serializer.validated_data['userPw']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            extended_user = UserInfo.objects.get(user_id=user)
            token_string = str(extended_user.jwt_token)
            return Response(data=json.dumps({'result': "true", "jwt": token_string}), status=200)
        else:
            return Response(data=json.dumps({'result': "false", "jwt": "Invalid", "errmsg": "Invalid login credentials"}), status=400)
    
    @action(detail=False, methods=['get'])
    def islogin(request):
        content= json.loads(request.body)
        token= content['jwtToken'].encode('utf-8')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        try:
            user = User.objects.get(username=payload["user_id"])
        except:
            return Response(data=json.dumps({'result': "false", "errmsg": "User not found"}), status=400)
        if user is not None and request.user.is_authenticated:
            extended_user = UserInfo.objects.get(user_id=user)
            return Response(data=json.dumps({'userId':user.username,
                                            'userPw':user.password,    
                                            'userNick':extended_user.nickname,
                                            'userRole':extended_user.user_role}), status=200)
        else:
            return Response(data=json.dumps({'result': "false", "errmsg": "Does not login yet"}), status=400)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        content = json.loads(request.body)
        auth.logout(request)
        return Response(data=json.dumps({'result': "true"}), status=200)
    
    @action(detail=False, methods=['delete'])
    def withdraw_account(request):
        content= json.loads(request.body)
        token= content['jwtToken'].encode('utf-8')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        try:
            user = User.objects.get(username=payload["user_id"])
        except:
            return Response(data=json.dumps({'result': "false", "errmsg": "User not found"}), status=400)
        
        if user is not None:
            extended_user = UserInfo.objects.get(user_id=user)
            extended_user.jwt_token.delete()
            extended_user.user.delete()
            extended_user.delete()
            return Response(data=json.dumps({'result': "true"}), status=200)
        else:
            return Response(data=json.dumps({'result': "false", "errmsg": "User not found"}), status=400)

    @action(detail=False, methods=['patch'])
    def pwchange(self, request):
        content= json.loads(request.body)
        token= content['jwtToken'].encode('utf-8')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = authenticate(request, username=payload["user_id"], password=content["userPw"])
        if user is not None:
            user.set_password(content["newPw"])
            user.save()
            return Response(data=json.dumps({'result': "true"}), status=200)
        return Response(data=json.dumps({'result': "false", "errmsg": "User not found"}), status=400)
    
    @action(detail=False, methods=['post'])
    def pwreset(self, request):
        content= json.loads(request.body)
        username = content['userId']
        try:
            user = User.objects.get(username=username)
        except:
            return Response(data=json.dumps({'result': "false", "errmsg": "User not found"}), status=400)
        
        if user is not None:
            validation_code = User.objects.make_random_password(length=20, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
            extended_user = UserInfo.objects.get(user_id=user)
            extended_user.validation_code = validation_code
            extended_user.save()
            pwreset_page = f'http://localhost:8000/users/pwreset_with_validation/?user={username}&validation={validation_code}'         ##### The url must be changed before release.!!!!!!!!!!!!!!!!
            send_mail(subject="Email for password reset",message=f"If you are requested to change your password, refer to here {pwreset_page}\n Otherwise, ignore it", from_email="e.learning.platform.team@gmail.com", recipient_list=[user.username],fail_silently=False)
            return Response(data=json.dumps({'result': "true"}), status=200)
        else:
            return Response(data=json.dumps({'result': "false", "errmsg": "User not found"}), status=400)

    @action(detail=False, methods=['get'])
    def pwreset_with_validation(request):
        username= request.GET.get('user')
        validation_code = request.GET.get('validation') 
        try:
            user = User.objects.get(username=username)
        except:
            return Response(data=json.dumps({'result': "false", "errmsg": "Invalid page"}), status=400)
        
        if user is not None:
            extended_user = UserInfo.objects.get(user_id=user)
            if extended_user.validation_code == validation_code:
                temp_password = User.objects.make_random_password(length=20, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
                user.set_password(temp_password)
                user.save()
                extended_user.validation_code = User.objects.make_random_password(length=20, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
                extended_user.save()
                return Response(data=json.dumps({'result': f'Your password is reset to {temp_password}'}), status=200)
            else:
                return Response(data=json.dumps({'result': "false", "errmsg": "Invalid page"}), status=400)
        else:
            return Response(data=json.dumps({'result': "false", "errmsg": "Invalid page"}), status=400)