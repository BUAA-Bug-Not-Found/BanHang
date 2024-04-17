import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import *
from .utils.check_user import generate_jwt_token, check_user

@api_view(['POST'])
def login(request):
    #!!!!!!!!这里还要修改，添加异常情况处理！！！！！！
    request_dict = json.loads(request.body.decode('utf-8'))
    username = request_dict['username']
    password = request_dict['password']

    user = User.objects.get(username=username, password=password)

    if user is None:
        return Response({'error': 'Invalid username or password'}, status=400)

    return Response({'token': generate_jwt_token(user.uid, user.username)})

@api_view(['POST'])
def register(request):
    #!!!!!!!!这里还要修改，添加异常情况处理！！！！！！
    request_dict = json.loads(request.body.decode('utf-8'))
    username = request_dict['username']
    password = request_dict['password']

    User(username=username, password=password).save()
    return Response({'status': 'Success'})

@api_view(['POST'])
@check_user
def demo(request, username):
    #这个无所谓
    return Response({})
