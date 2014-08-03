# Create your views here.

from backend.personal.models import User, UserState
from backend.univinfo.models import University, Major
from backend.personal.serializers import RegisterSerializer, UserStateSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.datastructures import MultiValueDictKeyError

def authenticated(method):
    def wrapper(request):
        try:
            token = request.DATA['token']
        except Exception:
            ret = produceRetCode('fail', 'token required')
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)
        try:
            state = UserState.objects.get(token=token)
        except UserState.DoesNotExist:
            ret = produceRetCode('fail', 'user did not login')
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=state.user.id)
        except User.DoesNotExist:
            ret = produceRetCode('error', 'database inconsistent')
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)
        request.DATA['user'] = user
        return method(request)
    return wrapper

@api_view(['GET', 'POST'])
def register(request):
    if request.method == 'POST':
        try:
            email = request.DATA['email']
        except MultiValueDictKeyError:
            ret = produceRetCode('fail', 'email is required')
            return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            user = User.objects.get(email = email)
            ret = produceRetCode('fail', 'email already exist')
            return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)
        except User.DoesNotExist:
            pass

        try:
            universityname = request.DATA['university']
        except KeyError:
            universityname = 'Unknown'
        try:
            university = University.objects.get(shortname = universityname)
        except University.DoesNotExist:
            university = University.objects.get(shortname = "Unknown")

        try:
            majorname = request.DATA['major']
        except KeyError:
            majorname = 'Unknown'
        try:
            major = Major.objects.get(shortname = majorname)
        except University.DoesNotExist:
            major = Major.objects.get(shortname = "Unknown")

        request.DATA['university'] = university.id
        request.DATA['major'] = major.id
        serializer = RegisterSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            ret = produceRetCode("success")
            return Response(ret, status=status.HTTP_201_CREATED)
        else:
            ret = produceRetCode('fail', 'register data format error', request.DATA)
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        users = User.objects.all()
        serializer = RegisterSerializer(users, many=True)
        ret = produceRetCode("success", '', serializer.data)
        return Response(ret, status=status.HTTP_200_OK)

import time
import hashlib
"""
login module:

This module is for ordinary login, not include OAuth function

input: email and password
response: status, message, and data['token']

Following circumstances may cause 'fail':
1, user_email doesn't exist in the user table
2, password doesn't match with the database
3, the user already logged in

"""
@api_view(['POST'])
def login(request):
    try:
        email = request.DATA['email']
    except Exception:
        ret = produceRetCode('fail', 'email required')
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email = email)
    except User.DoesNotExist:
        ret = produceRetCode('fail', 'user did not register')
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    m = hashlib.md5()
    m.update(email)
    m.update(time.strftime("%y%m%d%H%M%S",time.localtime()))
    token = m.hexdigest()
    # insure the token is unique
    while True:
        try:
            user_state = UserState.objects.get(token=token)
            m.update(time.strftime("%y%m%d%H%M%S",time.localtime()))
            token = m.hexdigest()
            continue
        except UserState.DoesNotExist:
            break
    stateData = {}
    stateData['user']  = user.id
    stateData['token'] = token
    stateData['ip']    = ip
    if request.DATA['password'] == user.password:
        ret = produceRetCode('success')
        serializer = UserStateSerializer(data=stateData)
        if serializer.is_valid():
            serializer.save()
            ret = produceRetCode('success','',stateData)
            return Response(ret, status=status.HTTP_200_OK)
        else:
            ret = produceRetCode('error', 'invalid UserState data')
            return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        ret = produceRetCode('fail','invalid email or password')
        return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)


"""
logout module:

input: token (got when login)
response: status, message
"""
@api_view(['POST'])
@authenticated
def logout(request):
    token = request.DATA['token']
    user_state = UserState.objects.get(token=token)
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
2, message (return error information when request fail)

"""
@api_view(['POST'])
@authenticated
def edit(request):
    user = request.DATA['user']
    try:
        if user.password == request.DATA['password']:
            pass
        else:
            ret = produceRetCode("fail", "invalid password")
            return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)
    except KeyError:
        ret = produceRetCode("fail", "password required")
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)
    try:
        if user.email == request.DATA['email']:
            pass
        else:
            ret = produceRetCode("fail", "email can not be changed")
            return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)
    except KeyError:
        ret = produceRetCode("fail", "email required")
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)
    try:
        universityname = request.DATA['university']
    except KeyError:
        universityname = 'Unknown'
    try:
        university = University.objects.get(shortname = universityname)
    except University.DoesNotExist:
        university = University.objects.get(shortname = "Unknown")

    try:
        majorname = request.DATA['major']
    except KeyError:
        majorname = 'Unknown'
    try:
        major = Major.objects.get(shortname = majorname)
    except University.DoesNotExist:
        major = Major.objects.get(shortname = "Unknown")

    request.DATA['university'] = university.id
    request.DATA['major'] = major.id

    serializer = RegisterSerializer(user, data = request.DATA)
    if serializer.is_valid():
        serializer.save()
        ret = produceRetCode('success')
        return Response(ret, status=status.HTTP_200_OK)
    else:
        ret = produceRetCode('fail', 'user info format error')
        return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)


"""
edit password module:

input: token, old_password, new_password
response: the same with edit module
"""
@api_view(['POST'])
@authenticated
def editPw(request):
    user = request.DATA['user']
    if user.password == request.DATA['old_password']:
        user.password = request.DATA['new_password']
        user.save()
        ret = produceRetCode('success')
        return Response(ret, status=status.HTTP_200_OK)
    else:
        ret = produceRetCode('fail', 'invalid password')
        return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)

def produceRetCode(status = "error", message = "", data = []):
    ret = {}
    ret['status'] = status
    if message:
        ret['message']   = message
    if data:
        ret['data']   = data
    return ret