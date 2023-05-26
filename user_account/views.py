from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import jwt
from datetime import datetime, timedelta
from django.conf import settings

from .models import UserInfo, JWTToken
# Create your views here.

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
    #jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])


@method_decorator(csrf_exempt, name="dispatch")
def signup(request):
    if request.method == 'POST':
        content= json.loads(request.body)
        user = User.objects.create_user(
            username = content['email'],
            password = content['password'],
        )
        new_jwt_token = generate_jwt_token(user, content['email'])
        extended_user = UserInfo.objects.create(
            user = user,
            jwt_token = new_jwt_token,
            nickname = "test nickname"
        )
        auth.login(request, user)
        return HttpResponse(json.dumps({'result': "true", 'nickname': extended_user.nickname}))
    return HttpResponse(json.dumps({'result': "false"}))

@method_decorator(csrf_exempt, name="dispatch")
def login(request):
    if request.method == 'POST':
        content= json.loads(request.body)
        username = content['email']
        password = content['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            extended_user = UserInfo.objects.get(user_id_id=user)
            return HttpResponse(json.dumps({'result': "true", 'nickname': extended_user.nickname}))
        else:
            return HttpResponse(json.dumps({'result': "false"}))
    else:
        return HttpResponse(json.dumps({'result': "false"}))

def logout(request):
    auth.logout(request)
    return HttpResponse(json.dumps({'result': "true"}))

def home(request):
    return HttpResponse(json.dumps({'result': "true"}))