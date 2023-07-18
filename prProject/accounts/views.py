from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
import requests
from prProject.settings import SOCIAL_OUTH_CONFIG
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

def home(request) :
    return render(request, 'main.html')

def signup(request) :
    if request.method == 'POST' :
        username = request.POST['username']
        password = password=request.POST['password']
        # username이 같은게 있으면 bad_join.html
        if User.objects.filter(username=username).exists():
            return render(request, 'bad_join.html')
        user = auth.authenticate(request, username=username, password=password)
        
        if (user is None) and (request.POST['password'] == request.POST['repeat']) :
            new_user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            auth.login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            print("회원가입 성공")
            return redirect('playlistApp:request_board')
        else :
            return render(request, 'bad_join.html')
    else :
        return render(request, 'signup.html')

def login(request) :
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)

        if user is not None :
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            print("로그인 성공")
            return redirect('playlistApp:request_board')
        else :
            return render(request, 'bad_login.html')
    else :   
        return render(request, 'login.html')
    
def logout(request) :
    auth.logout(request)
    return redirect('home')


@api_view(['GET'])
@permission_classes([AllowAny, ])
def kakao_get_login(request):
    CLIENT_ID = SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY']
    REDIRECT_URL = SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI']
    url = "https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={0}&redirect_uri={1}".format(
        CLIENT_ID, REDIRECT_URL)
    res = redirect(url)
    return res


@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_user_info(reqeust):
    CODE = reqeust.query_params['code']
    url = "https://kauth.kakao.com/oauth/token"
    res = {
        'grant_type': 'authorization_code',
        'client_id': SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY'],
        'redirect_url': SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI'],
        'client_secret': SOCIAL_OUTH_CONFIG['KAKAO_SECRET_KEY'],
        'code': CODE
    }
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    response = requests.post(url, data=res, headers=headers)
    token_json = response.json()
    user_url = "https://kapi.kakao.com/v2/user/me"
    auth = "Bearer " + token_json['access_token']
    HEADER = {
        "Authorization": auth,
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    res = requests.get(user_url, headers=HEADER)
    print(response.json())
    return Response(res.text)
