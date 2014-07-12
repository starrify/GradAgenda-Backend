# Create your views here.

from backend.personal.models import User, UserState
from backend.personal.serializers import RegisterSerializer, UserStateSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

"""
register module:

input: data refer to personal.models
response:
1,status ("success" means request successfully)
2,info   (possible reason for any "fail", such as user already exist, lost required information and so on)

'GET' API is just for testing
"""
@api_view(['GET', 'POST'])
def register(request):
    if request.method == 'POST':
        email = request.DATA['email']
        try:
            user = User.objects.get(email = email)
            ret = produceRetCode('fail', 'the user_name exist')
            return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)
        except User.DoesNotExist:
            pass
        serializer = RegisterSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        users = User.objects.all()
        serializer = RegisterSerializer(users, many=True)
        return Response(serializer.data)

import time
import hashlib
"""
login module:

This module is for ordinary login, not include OAuth function

input: email and password
response: status, info, and data['token']

Following circumstances may cause 'fail':
1, user_email doesn't exist in the user table
2, password doesn't match with the database
3, the user already logged in

"""
@api_view(['POST'])
def login(request):
    email = request.DATA['email']
    try:
        user = User.objects.get(email = email)
    except User.DoesNotExist:
        ret = produceRetCode('error', 'user does not exist')
        return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    m = hashlib.md5()
    m.update(email)
    m.update(time.strftime("%y%m%d%H%M%S",time.localtime()))
    token = m.hexdigest()
    stateData = {}
    stateData['user']  = user.id
    stateData['token'] = token
    stateData['ip']    = ip
    if request.DATA['password'] == user.password:
        ret = produceRetCode('success')
        try:
            state = UserState.objects.get(user = user.id, ip = ip)
            if state:
                ret = produceRetCode('error','user already online')
                return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)
        except UserState.DoesNotExist:
            print stateData
            serializer = UserStateSerializer(data=stateData)
            if serializer.is_valid():
                serializer.save()
                ret = produceRetCode('success','return token',stateData)
                return Response(ret, status=status.HTTP_200_OK)
            else:
                ret = produceRetCode('error', 'invalid UserState data')
                return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        ret = produceRetCode('fail','user_email or password error')
        return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)


"""
logout module:

input: token (got when login)
response: status, info
"""
@api_view(['POST'])
def logout(request):
    token = request.DATA['token']
    try:
        user_state = UserState.objects.get(token=token)
    except UserState.DoesNotExist:
        ret = produceRetCode('fail', 'the user has not logged in')
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)
    user_state.delete()
    ret = produceRetCode('success','logged out successfully')
    return Response(ret, status=status.HTTP_204_NO_CONTENT)

"""
edit module(password edit not included):
input:
1, token
2, data (refer to personal.models.user)

response:
1, stauts (success, fail or error)
2, info (return error information when request fail)

"""
@api_view(['POST'])
def edit(request):
    token = request.DATA['token']
    try:
        state = UserState.objects.get(token = token)
    except UserState.DoesNotExist:
        ret = produceRetCode("fail", "user doesn't login")
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(id = state.user.id)
    except User.DoesNotExist:
        ret = produceRetCode("error", "database inconsistent")
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)
    if user.password == request.DATA['data']['password']:
        pass
    else:
        ret = produceRetCode("error", "invalid operation")
        return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)
    if request.method == "POST":
        serializer = RegisterSerializer(user, data = request.DATA['data'])
        if serializer.is_valid():
            serializer.save()
            ret = produceRetCode('success')
            return Response(ret)
        ret = produceRetCode('fail', 'user info error')
        return Response(ret)


"""
edit password module:

input: token, old_password, new_password
response: the same with edit module
"""
@api_view(['POST'])
def editPw(request):
    token = request.DATA['token']
    try:
        state = UserState.objects.get(token = token)
    except UserState.DoesNotExist:
        ret = produceRetCode("fail", "user doesn't login")
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(id = state.user.id)
    except User.DoesNotExist:
        ret = produceRetCode("error", "database inconsistent")
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)
    if user.password == request.DATA['old_password']:
        user.password = request.DATA['new_password']
        user.save()
        ret = produceRetCode('success')
        return Response(ret, status=status.HTTP_200_OK)
    else:
        ret = produceRetCode('fail', 'Password error')
        return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)



def produceRetCode(status = "error", info = "", data = []):
    ret = {}
    ret['status'] = status
    if info:
        ret['info']   = info
    if data:
        ret['data']   = data
    return ret

