# Create your views here.

from backend.personal.models import User, UserState
from backend.personal.serializers import RegisterSerializer, UserStateSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.personal.auth import authenticated
from backend.personal.common import produceRetCode, MESSAGES
"""
register module:

input: data refer to personal.models
response:
1,status ("success" means request successfully)
2,message   (possible reason for any "fail", such as user already exist, lost required information and so on)

'GET' API is just for testing
"""

@api_view(['GET', 'POST'])
def register(request):
    if request.method == 'POST':
        email = request.DATA['email']
        try:
            user = User.objects.get(email = email)
            ret = produceRetCode('fail', MESSAGES['fail_user_exist'])
            return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)
        except User.DoesNotExist:
            pass
        serializer = RegisterSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            ret = produceRetCode("success")
            return Response(ret, status=status.HTTP_201_CREATED)
        else:
            ret = produceRetCode('fail', MESSAGES['fail_user_data'])
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)
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
response: status, message, and data['token']

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
        ret = produceRetCode('fail', MESSAGES['fail_user_notExist'])
        return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)
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
            ret = produceRetCode('error', MESSAGES['error_unknown'])
            return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        ret = produceRetCode('fail', MESSAGES['fail_emailOrPw'])
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
    token = request.DATA['token']
    try:
        state = UserState.objects.get(token = token)
        user = User.objects.get(id = state.user.id)
    except User.DoesNotExist:
        ret = produceRetCode("error", MESSAGES['error_database'])
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)
    if user.password == request.DATA['data']['password']:
        pass
    else:
        ret = produceRetCode("fail", MESSAGES['fail_illegal'])
        return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)
    serializer = RegisterSerializer(user, data = request.DATA['data'])
    if serializer.is_valid():
        serializer.save()
        ret = produceRetCode('success')
        return Response(ret, status = status.HTTP_200_OK)
    ret = produceRetCode('fail', MESSAGES['fail_user_data'])
    return Response(ret)


"""
edit password module:

input: token, old_password, new_password
response: the same with edit module
"""
@api_view(['POST'])
@authenticated
def editPw(request):
    token = request.DATA['token']
    try:
        state = UserState.objects.get(token = token)
    except UserState.DoesNotExist:
        ret = produceRetCode("fail", MESSAGES['fail_notLogin'])
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(id = state.user.id)
    except User.DoesNotExist:
        ret = produceRetCode("error", MESSAGES['error_database'])
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)
    if user.password == request.DATA['old_password']:
        user.password = request.DATA['new_password']
        user.save()
        ret = produceRetCode('success')
        return Response(ret, status=status.HTTP_200_OK)
    else:
        ret = produceRetCode('fail', MESSAGES['fail_emailOrPw'])
        return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)





