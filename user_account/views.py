from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json, jwt, logging, os, zipfile
from datetime import datetime, timedelta
from django.conf import settings
from .models import UserInfo, JWTToken
from django.core.mail import send_mail
from rest_framework import viewsets, parsers, generics
from .serializers import UserInfoSerializer, UserSerializer
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
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
   
    JWT = JWTToken.objects.create(
        token = token,
        user = user
    )

    # Return the generated token as a string
    return JWT

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=False, methods=['post'])
    def signup(self, request):
        content = json.loads(request.body)
        try:
            user = User.objects.create_user(
            username = content['userId'],
            password = content['userPw'],
            )
            user.save()
        except:
            return HttpResponse(json.dumps({'result': "false", "jwt": "Invaild", "errmsg": "Signup already done with same Id"}))
       
        JWT = generate_jwt_token(user, content['userId'])
    
        extended_user = UserInfo.objects.create(
            user = user,
            jwt_token = JWT,
            nickname = user.username.split("@")[0]
        )
        extended_user.save()
        return HttpResponse(json.dumps({'result': "true", "jwt": JWT.token}))  
          
    @action(detail=False, methods=['post'])
    def login(self, request):
        content = json.loads(request.body)
        user = authenticate(request, username=content['userId'], password=content['userPw'])
        if user is not None:
            auth.login(request, user)
            extended_user = UserInfo.objects.get(user_id=user)
            token_string = str(extended_user.jwt_token)
            return HttpResponse(json.dumps({'result': "true", "jwt": token_string}))
        else:
            return HttpResponse(json.dumps({'result': "false", "jwt": "Invalid", "errmsg": "Invalid login credentials"}))

    @action(detail=False, methods=['get'])
    def islogin(request):
        content= json.loads(request.body)
        token= content['jwtToken'].encode('utf-8')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        try:
            user = User.objects.get(username=payload["user_id"])
        except:
            return HttpResponse(json.dumps({'result': "false", "errmsg": "User not found"}))
        if user is not None and request.user.is_authenticated:
            extended_user = UserInfo.objects.get(user_id=user)
            return HttpResponse(json.dumps({'userId':user.username,
                                            'userPw':user.password,    
                                            'userNick':extended_user.nickname,
                                            'userRole':extended_user.user_role}))
        else:
            return HttpResponse(json.dumps({'result': "false", "errmsg": "Does not login yet"}))

    @action(detail=False, methods=['post'])
    def logout(self, request):
        content = json.loads(request.body)
        auth.logout(request)
        return HttpResponse(json.dumps({'result': "true"}))
    
    @action(detail=False, methods=['delete'])
    def withdraw_account(request):
        content= json.loads(request.body)
        token= content['jwtToken'].encode('utf-8')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        try:
            user = User.objects.get(username=payload["user_id"])
        except:
            return HttpResponse(json.dumps({'result': "false", "errmsg": "User not found"}))
        
        if user is not None:
            extended_user = UserInfo.objects.get(user_id=user)
            extended_user.jwt_token.delete()
            extended_user.user.delete()
            extended_user.delete()
            return HttpResponse(json.dumps({'result': "true"}))
        else:
            return HttpResponse(json.dumps({'result': "false", "errmsg": "User not found"}))

    @action(detail=False, methods=['patch'])
    def pwchange(self, request):
        content= json.loads(request.body)
        token= content['jwtToken'].encode('utf-8')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = authenticate(request, username=payload["user_id"], password=content["userPw"])
        if user is not None:
            user.set_password(content["newPw"])
            user.save()
            return HttpResponse(json.dumps({'result': "true"}))
        return HttpResponse(json.dumps({'result': "false", "errmsg": "User not found"}))
    
    @action(detail=False, methods=['post'])
    def pwreset(self, request):
        content= json.loads(request.body)
        username = content['userId']
        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponse(json.dumps({'result': "false", "errmsg": "User not found"}))
        
        if user is not None:
            validation_code = User.objects.make_random_password(length=20, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
            extended_user = UserInfo.objects.get(user_id=user)
            extended_user.validation_code = validation_code
            extended_user.save()
            pwreset_page = f'http://localhost:8000/users/pwreset_with_validation/?user={username}&validation={validation_code}'         ##### The url must be changed before release.!!!!!!!!!!!!!!!!
            send_mail(subject="Email for password reset",message=f"If you are requested to change your password, refer to here {pwreset_page}\n Otherwise, ignore it", from_email="e.learning.platform.team@gmail.com", recipient_list=[user.username],fail_silently=False)
            return HttpResponse(json.dumps({'result': "true"}))
        else:
            return HttpResponse(json.dumps({'result': "false", "errmsg": "User not found"}))

    @action(detail=False, methods=['get'])
    def pwreset_with_validation(request):
        username= request.GET.get('user')
        validation_code = request.GET.get('validation') 
        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponse(json.dumps({'result': "false", "errmsg": "Invalid page"}))
        
        if user is not None:
            extended_user = UserInfo.objects.get(user_id=user)
            if extended_user.validation_code == validation_code:
                temp_password = User.objects.make_random_password(length=20, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
                user.set_password(temp_password)
                user.save()
                extended_user.validation_code = User.objects.make_random_password(length=20, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
                extended_user.save()
                return HttpResponse(json.dumps({'result': f'Your password is reset to {temp_password}'}))
            else:
                return HttpResponse(json.dumps({'result': "false", "errmsg": "Invalid page"}))
        else:
            return HttpResponse(json.dumps({'result': "false", "errmsg": "Invalid page"}))

class UserInfoViewset(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']

# def generate_jwt_token(user, user_id):
#     queryset = User.objects.all()
#     # Set the expiration time for the token (e.g., 1 day from now)
#     expiration = datetime.utcnow() + timedelta(days=1)

#     # Create the payload containing user information
#     payload = {
#         'user_id': user_id,
#         'exp': expiration,
#     }

#     # Generate the JWT token using the secret key defined in Django settings
#     token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
#     JWT = JWTToken.objects.create(
#         token = token,
#         user = user
#     )

#     # Return the generated token as a string
#     return JWT
#     #jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])


# @method_decorator(csrf_exempt, name="dispatch")
# def signup(request):
#         content= json.loads(request.body)
#         try:
#             user = User.objects.create_user(
#             username = content['userId'],
#             password = content['userPw'],
#             )
#             #logging.info(content)
#         except:
#             return HttpResponse(json.dumps({'result': "false", "jwt": "Invaild"})) # Check if the user already exists
#         new_jwt_token = generate_jwt_token(user, content['userId'])
#         extended_user = UserInfo.objects.create(
#             user = user,
#             jwt_token = new_jwt_token,
#             nickname = user.username.split("@")[0]
#         )
#         token_string = new_jwt_token.token.decode('utf-8')
#         auth.login(request, user)
#         return HttpResponse(json.dumps({'result': "true", "jwt": token_string}))
   
# @method_decorator(csrf_exempt, name="dispatch")
# def login(request):
#     if request.method == 'POST':
#         content= json.loads(request.body)
#         username = content['userId']
#         password = content['userPw']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             extended_user = UserInfo.objects.get(user_id=user)
#             token_string = extended_user.jwt_token.token.decode('utf-8')
#             return HttpResponse(json.dumps({'result': "true", "jwt": token_string}))
#         else:
#             return HttpResponse(json.dumps({'result': "false", "jwt": "Invaild"}))
#     else:
#         return HttpResponse(json.dumps({'result': "false", "jwt": "Invaild"}))

# @method_decorator(csrf_exempt, name="dispatch")
# def logout(request):
#     if request.method == 'PUT':
#         auth.logout(request)
#         return HttpResponse(json.dumps({'result': "true"}))
#     else:
#         return HttpResponse(json.dumps({'result': "false"}))

# @method_decorator(csrf_exempt, name="dispatch")
# def withdraw_account(request):
#     if request.method == 'DELETE':
#         content= json.loads(request.body)
#         token= content['jwt'].encode('utf-8')
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#         try:
#             user = User.objects.get(username=payload["user_id"])
#         except:
#             return HttpResponse(json.dumps({'result': "false"}))
        
#         if user is not None:
#             extended_user = UserInfo.objects.get(user_id=user)
#             extended_user.jwt_token.delete()
#             extended_user.user.delete()
#             extended_user.delete()
#             return HttpResponse(json.dumps({'result': "true"}))
#         else:
#             return HttpResponse(json.dumps({'result': "false"}))
#     else:
#         return HttpResponse(json.dumps({'result': "false"}))

# @method_decorator(csrf_exempt, name="dispatch")
# def home(request):
#     return HttpResponse(json.dumps({'result': "true"}))

# @method_decorator(csrf_exempt, name="dispatch")
# def pwchange(request):
#     if request.method == 'PUT':
#         content= json.loads(request.body)
#         token= content['jwt'].encode('utf-8')
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#         user = authenticate(request, username=payload["user_id"], password=content["userPw"])
#         if user is not None:
#             user.set_password(content["newPw"])
#             user.save()
#             return HttpResponse(json.dumps({'result': "true"}))
#         else:
#             return HttpResponse(json.dumps({'result': "false"}))
#     else:
#         return HttpResponse(json.dumps({'result': "false"}))
    
# @method_decorator(csrf_exempt, name="dispatch")
# def pwreset(request):
#     if request.method == 'POST':
#         content= json.loads(request.body)
#         username = content['userId']
#         try:
#             user = User.objects.get(username=username)
#         except:
#             return HttpResponse(json.dumps({'result': "false"}))
        
#         if user is not None:
#             validation_code = User.objects.make_random_password(length=20, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
#             extended_user = UserInfo.objects.get(user_id=user)
#             extended_user.validation_code = validation_code
#             extended_user.save()
#             pwreset_page = f'http://localhost:8000/user_account/pwreset_with_validation/?user={username}&validation={validation_code}'         ##### The url must be changed before release.!!!!!!!!!!!!!!!!
#             send_mail(subject="Email for password reset",message=f"If you are requested to change your password, refer to here {pwreset_page}\n Otherwise, ignore it", from_email="e.learning.platform.team@gmail.com", recipient_list=[user.username],fail_silently=False)
#             return HttpResponse(json.dumps({'result': "true"}))
#         else:
#             return HttpResponse(json.dumps({'result': "false"}))
#     else:
#         return HttpResponse(json.dumps({'result': "false"}))

# @method_decorator(csrf_exempt, name="dispatch")
# def pwreset_with_validation(request):
#     if request.method == 'GET':
#         username= request.GET.get('user')
#         validation_code = request.GET.get('validation') 
#         try:
#             user = User.objects.get(username=username)
#         except:
#             return HttpResponse(json.dumps({'result': "Invaild page"}))
        
#         if user is not None:
#             extended_user = UserInfo.objects.get(user_id=user)
#             if extended_user.validation_code == validation_code:
#                 temp_password = User.objects.make_random_password(length=20, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
#                 user.set_password(temp_password)
#                 user.save()
#                 extended_user.validation_code = User.objects.make_random_password(length=20, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
#                 extended_user.save()
#                 return HttpResponse(json.dumps({'result': f'Your password is reset to {temp_password}'}))
#             else:
#                 return HttpResponse(json.dumps({'result': "Invaild page"}))
#         else:
#             return HttpResponse(json.dumps({'result': "Invaild page"}))
#     else:
#         return HttpResponse(json.dumps({'result': "Invaild page"}))