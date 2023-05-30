from django.shortcuts import render, redirect
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
from django.http import FileResponse, JsonResponse
from django.core.files.temp import NamedTemporaryFile
# Create your views here.

def check_validity(request): ## If true => go ahead request, elif token => give back re-publish access token, else (None)=> login again
    access_token = request.COOKIES.get('token').encode('utf-8') # Access token stored in client cookie
    content= json.loads(request.body)
    refresh_token= content['jwt'].encode('utf-8')               # Refresh token stored in client local storage (Managing: front side work)
    
    if access_token.is_valid(): # Check if the access token is valid
        return True
    else:
        if refresh_token.is_valid():  # Check if the refresh token is valid to re-publish the access token
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
            try:
                user = User.objects.get(username=payload["user_id"])
            except:
                return None

            if user is not None:
                extended_user = UserInfo.objects.get(user_id=user)
                if extended_user.jwt_token == refresh_token:
                    new_access_token = generate_access_token(user, payload["user_id"])
                    return new_access_token  # Return new access token
            else:
                return None
        else:
            return None

def generate_access_token(user, user_id):
    expiration = datetime.utcnow() + timedelta(minutes=30)

    payload = {
        'user_id': user_id,
        'exp': expiration,
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    JWT = JWTToken.objects.create(
        token = token,
        user = user
    )
    return JWT

def generate_refresh_token(user, user_id):
    expiration = datetime.utcnow() + timedelta(days=14)

    payload = {
        'user_id': user_id,
        'exp': expiration,
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    JWT = JWTToken.objects.create(
        token = token,
        user = user
    )
    return JWT

@method_decorator(csrf_exempt, name="dispatch")
def signup(request):
    if request.method == 'POST':
        content= json.loads(request.body)
        try:
            user = User.objects.create_user(
            username = content['userId'],
            password = content['userPw'],
            )
        except:
            return HttpResponse(json.dumps({'result': "false"})) # Check if the user already exists
        
        extended_user = UserInfo.objects.create(
            user = user,
            jwt_token = None,
            nickname = "test nickname"
        )
        return HttpResponse(json.dumps({'result': "true"}))
    return HttpResponse(json.dumps({'result': "false"}))

@method_decorator(csrf_exempt, name="dispatch")
def login(request):
    if request.method == 'POST':
        content= json.loads(request.body)
        username = content['userId']
        password = content['userPw']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            access_token = generate_access_token(user, content['userId'])
            refresh_token = generate_refresh_token(user, content['userId'])

            extended_user = UserInfo.objects.get(user_id=user)
            extended_user.jwt_token = refresh_token
            extended_user.save()

            access_token_string = access_token.token.decode('utf-8')
            response = HttpResponse(json.dumps({'result': "true", 'jwt': refresh_token.token.decode('utf-8')}))
            response.set_cookie('token', access_token_string, httponly=True, samesite='Strict')
            return response                             ## Store access token in client cookie and store refresh token (jwt) in client local storage
        else:
            return HttpResponse(json.dumps({'result': "false", 'jwt': "Invalid"}))
    else:
        return HttpResponse(json.dumps({'result': "false", 'jwt': "Invalid"}))

@method_decorator(csrf_exempt, name="dispatch")
def logout(request):
    if request.method == 'PUT':
        auth.logout(request)
        token = request.COOKIES.get('token').encode('utf-8')

        access_token = JWTToken.objects.get(token=token)
        access_token.blacklist = True
        
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = User.objects.get(username=payload["user_id"])
        extended_user = UserInfo.objects.get(user_id=user)
        token_object = JWTToken.objects.get(token=extended_user.jwt_token.token)
        token_object.delete()
        extended_user.jwt_token = None

        response = HttpResponse(json.dumps({'result': "true"}))
        response.delete_cookie('token')
        return response
    else:
        return HttpResponse(json.dumps({'result': "false"}))

@method_decorator(csrf_exempt, name="dispatch")
def withdraw_account(request):
    valid = check_validity(request)
    response = HttpResponse()

    if valid == True:
        pass
    elif valid == None:
        return logout(request)
    else:
        new_access_token_string = valid.decode('utf-8')
        response.set_cookie('token', new_access_token_string, httponly=True, samesite='Strict')

    if request.method == 'DELETE':
        if valid == True:
            token = request.COOKIES.get('token').encode('utf-8')
        else:
            token = valid.encode('utf-8')
        
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        try:
            user = User.objects.get(username=payload["user_id"])
        except:
            response.content = json.dumps({'result': "false"})
            return response
        
        if user is not None:
            extended_user = UserInfo.objects.get(user_id=user)
            extended_user.jwt_token.delete()
            extended_user.user.delete()
            extended_user.delete()
            response.content = json.dumps({'result': "true"})
            return response
        else:
            response.content = json.dumps({'result': "false"})
            return response
    else:
        response.content = json.dumps({'result': "false"})
        return response

@method_decorator(csrf_exempt, name="dispatch")
def pwchange(request):
    valid = check_validity(request)
    response = HttpResponse()

    if valid == True:
        pass
    elif valid == None:
        return logout(request)
    else:
        new_access_token_string = valid.decode('utf-8')
        response.set_cookie('token', new_access_token_string, httponly=True, samesite='Strict')

    if request.method == 'PUT':
        content= json.loads(request.body)
        token= content['jwt'].encode('utf-8')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = authenticate(request, username=payload["user_id"], password=content["userPw"])
        if user is not None:
            user.set_password(content["newPw"])
            user.save()
            response.content= json.dumps({'result': "true"})
            return response
        else:
            response.content= json.dumps({'result': "false"})
            return response
    else:
        response.content= json.dumps({'result': "false"})
        return response
    
@method_decorator(csrf_exempt, name="dispatch")
def pwreset(request):
    valid = check_validity(request)
    response = HttpResponse()

    if valid == True:
        pass
    elif valid == None:
        return logout(request)
    else:
        new_access_token_string = valid.decode('utf-8')
        response.set_cookie('token', new_access_token_string, httponly=True, samesite='Strict')

    if request.method == 'POST':
        content= json.loads(request.body)
        username = content['userId']
        try:
            user = User.objects.get(username=username)
        except:
            response.content= json.dumps({'result': "false"})
            return response
        
        if user is not None:
            validation_code = User.objects.make_random_password(length=20, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
            extended_user = UserInfo.objects.get(user_id=user)
            extended_user.validation_code = validation_code
            extended_user.save()
            pwreset_page = f'http://localhost:8000/user_account/pwreset_with_validation/?user={username}&validation={validation_code}'         ##### The url must be changed before release.!!!!!!!!!!!!!!!!
            send_mail(subject="Email for password reset",message=f"If you are requested to change your password, refer to here {pwreset_page}\n Otherwise, ignore it", from_email="e.learning.platform.team@gmail.com", recipient_list=[user.username],fail_silently=False)
            response.content= json.dumps({'result': "true"})
            return response
        else:
            response.content= json.dumps({'result': "false"})
            return response
    else:
        response.content= json.dumps({'result': "false"})
        return response

@method_decorator(csrf_exempt, name="dispatch")
def pwreset_with_validation(request):
    if request.method == 'GET':
        username= request.GET.get('user')
        validation_code = request.GET.get('validation') 
        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponse(json.dumps({'result': "Invaild page"}))
        
        if user is not None:
            extended_user = UserInfo.objects.get(user_id=user)
            if extended_user.validation_code == validation_code:
                temp_password = User.objects.make_random_password(length=20, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
                user.set_password(temp_password)
                user.save()
                return HttpResponse(json.dumps({'result': f'Your password is reset to {temp_password}'}))
            else:
                return HttpResponse(json.dumps({'result': "Invaild page"}))
        else:
            return HttpResponse(json.dumps({'result': "Invaild page"}))
    else:
        return HttpResponse(json.dumps({'result': "Invaild page"}))

@method_decorator(csrf_exempt, name="dispatch")
def islogin(request):
    if check_validity(request) is not None:
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
