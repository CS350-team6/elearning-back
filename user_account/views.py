from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from .models import UserInfo
# Create your views here.

@method_decorator(csrf_exempt, name="dispatch")
def signup(request):
    if request.method == 'POST':
        content= json.loads(request.body)
        user = User.objects.create_user(
            username = content['email'],
            password = content['password'],
        )
        extended_user = UserInfo.objects.create(
            user_id = user,
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