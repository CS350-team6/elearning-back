from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json, jwt
from datetime import datetime, timedelta
from django.conf import settings
from .models import UserInfo, JWTToken
from django.core.mail import send_mail
from rest_framework import viewsets, parsers, generics
from .serializers import UserInfoSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=False, methods=['post'])
    def login(self, request):
        content = json.loads(request.body)
        user = authenticate(email=content['email'], password=content['password'])
        if user is not None:
            login(request, user)
            JWT = generate_jwt_token(user, user.id)
            return Response(JWT.token, status=200)
        else:
            return Response("Invalid login credentials", status=400)
        
    @action(detail=False, methods=['post'])
    def signup(self, request):
        content = json.loads(request.body)
        user = User.objects.create_user(content['username'], content['email'], content['password'])
        user.save()
        # userinfo = UserInfo.objects.create(
        #     user = user,
        #     nickname = content['nickname']
        # )
        # userinfo.save()
        JWT = generate_jwt_token(user, user.id)
        return Response(JWT.token, status=200)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        content = json.loads(request.body)
        JWT = JWTToken.objects.get(token=content['token'])
        JWT.delete()
        return Response("Success", status=200)
    
    @action(detail=False, methods=['post'])
    def check(self, request):
        content = json.loads(request.body)
        try:
            JWT = JWTToken.objects.get(token=content['token'])
            return Response("Success", status=200)
        except:
            return Response("Fail", status=400)
        
    @action(detail=False, methods=['patch'])
    def pwchange(self, request):
        content= json.loads(request.body)
        token= content['jwt'].encode('utf-8')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = authenticate(request, username=payload["user_id"], password=content["userPw"])
        if user is not None:
            user.set_password(content["newPassword"])
            user.save()
            return Response(json.dumps({'result': "true"}), status=200)
        return Response(json.dumps({'result': "false"}), status=400)
    
    @action(detail=False, methods=['post'])
    def pwreset(self, request):
        content= json.loads(request.body)
        token= content['jwt'].encode('utf-8')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        try:
            user = User.objects.get(username=payload["user_id"])
        except:
            return Response(json.dumps({'result': "false"}), status=400)
        
        if user.username==content["username"]:
            temp_password = User.objects.make_random_password()
            user.set_password(temp_password)
            user.save()
            send_mail(subject="Email for password reset",message=f"Your password is reset to {temp_password}", from_email="e.learning.platform.team@gmail.com", recipient_list=[user.username],fail_silently=False)
            return Response(json.dumps({'result': "true"}), status=200)
        return Response(json.dumps({'result': "false"}), status=400)

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
#     if request.method == 'POST':
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
#             nickname = "test nickname"
#         )
#         #print("TEST")
#         #print(str(new_jwt_token.token))
#         #token_string = str(new_jwt_token.token).split("'")[1]
#         token_string = str(new_jwt_token.token)
#         auth.login(request, user)
#         return HttpResponse(json.dumps({'result': "true", "jwt": token_string}))
#     return HttpResponse(json.dumps({'result': "false", "jwt": "Invaild"}))

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
#             #token_string = str(extended_user.jwt_token.token).split("'")[1]
#             token_string = str(extended_user.jwt_token.token)
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
#         token= content['jwt'].encode('utf-8')
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#         try:
#             user = User.objects.get(username=payload["user_id"])
#         except:
#             return HttpResponse(json.dumps({'result': "false"}))
        
#         if user.username==content["userId"]:
#             temp_password = User.objects.make_random_password()
#             user.set_password(temp_password)
#             user.save()
#             send_mail(subject="Email for password reset",message=f"Your password is reset to {temp_password}", from_email="e.learning.platform.team@gmail.com", recipient_list=[user.username],fail_silently=False)
#             return HttpResponse(json.dumps({'result': "true"}))
#     else:
#         return HttpResponse(json.dumps({'result': "false"}))