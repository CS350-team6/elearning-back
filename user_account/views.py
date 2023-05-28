from django.shortcuts import render, redirect
import zipfile

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
from django.http import FileResponse
from django.core.files.temp import NamedTemporaryFile
import logging
import os
from django.http import JsonResponse
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
        try:
            user = User.objects.create_user(
            username = content['userId'],
            password = content['userPw'],
            logging.info(content)
        except:
            return HttpResponse(json.dumps({'result': "false", "jwt": "Invaild"})) # Check if the user already exists
        new_jwt_token = generate_jwt_token(user, content['userId'])
        extended_user = UserInfo.objects.create(
            user = user,
            jwt_token = new_jwt_token,
            nickname = "test nickname"
        )
        token_string = str(new_jwt_token.token).split("'")[1]
        auth.login(request, user)
        return HttpResponse(json.dumps({'result': "true", "jwt": token_string}))
    return HttpResponse(json.dumps({'result': "false", "jwt": "Invaild"}))

@method_decorator(csrf_exempt, name="dispatch")
def login(request):
    if request.method == 'POST':
        content= json.loads(request.body)
        username = content['userId']
        password = content['userPw']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            extended_user = UserInfo.objects.get(user_id=user)
            token_string = str(extended_user.jwt_token.token).split("'")[1]
            return HttpResponse(json.dumps({'result': "true", "jwt": token_string}))
        else:
            return HttpResponse(json.dumps({'result': "false", "jwt": "Invaild"}))
    else:
        return HttpResponse(json.dumps({'result': "false", "jwt": "Invaild"}))

@method_decorator(csrf_exempt, name="dispatch")
def logout(request):
    if request.method == 'PUT':
        auth.logout(request)
        return HttpResponse(json.dumps({'result': "true"}))
    else:
        return HttpResponse(json.dumps({'result': "false"}))

@method_decorator(csrf_exempt, name="dispatch")
def withdraw_account(request):
    if request.method == 'DELETE':
        content= json.loads(request.body)
        token= content['jwt'].encode('utf-8')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        try:
            user = User.objects.get(username=payload["user_id"])
        except:
            return HttpResponse(json.dumps({'result': "false"}))
        
        if user is not None:
            extended_user = UserInfo.objects.get(user_id=user)
            extended_user.jwt_token.delete()
            extended_user.user.delete()
            extended_user.delete()
            return HttpResponse(json.dumps({'result': "true"}))
        else:
            return HttpResponse(json.dumps({'result': "false"}))
    else:
        return HttpResponse(json.dumps({'result': "false"}))

@method_decorator(csrf_exempt, name="dispatch")
def home(request):
    return HttpResponse(json.dumps({'result': "true"}))

@method_decorator(csrf_exempt, name="dispatch")
def pwchange(request):
    if request.method == 'PUT':
        content= json.loads(request.body)
        token= content['jwt'].encode('utf-8')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = authenticate(request, username=payload["user_id"], password=content["userPw"])
        if user is not None:
            user.set_password(content["newPw"])
            user.save()
            return HttpResponse(json.dumps({'result': "true"}))
        else:
            return HttpResponse(json.dumps({'result': "false"}))
    else:
        return HttpResponse(json.dumps({'result': "false"}))
    
@method_decorator(csrf_exempt, name="dispatch")
def pwreset(request):
    if request.method == 'POST':
        content= json.loads(request.body)
        token= content['jwt'].encode('utf-8')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        try:
            user = User.objects.get(username=payload["user_id"])
        except:
            return HttpResponse(json.dumps({'result': "false"}))
        
        if user.username==content["userId"]:
            temp_password = User.objects.make_random_password()
            user.set_password(temp_password)
            user.save()
            send_mail(subject="Email for password reset",message=f"Your password is reset to {temp_password}", from_email="e.learning.platform.team@gmail.com", recipient_list=[user.username],fail_silently=False)
            return HttpResponse(json.dumps({'result': "true"}))
    else:
        return HttpResponse(json.dumps({'result': "false"}))

@method_decorator(csrf_exempt, name="dispatch")
def searchTest(request):
    if request.method == 'POST':
        
        return HttpResponse(json.dumps({'result': "true", "title":["A","B","C"]}))
    return HttpResponse(json.dumps({'result': "false"}))

@method_decorator(csrf_exempt, name="dispatch")
def uploadTest(request):
    if request.method == 'POST':
        content= json.loads(request.body)
        print(content)
        return HttpResponse(json.dumps({'result': "true", "thumb":"path"}))
    return HttpResponse(json.dumps({'result': "false"}))

@method_decorator(csrf_exempt, name="dispatch")
def videoTest(request):
    if request.method == 'GET':
        
        lecture = request.GET.get('lecture')
      
        video_dir = '../../Downloads/'
        video_files = [f for f in os.listdir(video_dir) if lecture in f and f.endswith('.mp4')]
        print(video_files)
        return JsonResponse(video_files, safe=False)
