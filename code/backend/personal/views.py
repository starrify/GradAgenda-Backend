# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS

from backend.personal.models import User, UserState
from backend.personal.serializers import RegisterSerializer, UserStateSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
            serializer = UserStateSerializer(data=stateData)
            if serializer.is_valid():
                serializer.save()
                ret = produceRetCode('success','return token',stateData)
                return Response(ret, status=status.HTTP_200_OK)
    else:
        ret = produceRetCode('fail','user_name or password error')
        return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['POST'])
def edit(request):
    email = request.DATA['email']
    try:
        user = User.objects.get(email = email)
    except User.DoesNotExist:
        ret = produceRetCode("error", "user doesn't exist")
        return Response(ret)
    if request.method == "POST":
        serializer = RegisterSerializer(user, data = request.DATA)
        if serializer.is_valid():
            serializer.save()
            ret = produceRetCode('success')
            return Response(ret)
        ret = produceRetCode('fail', 'user info error')
        return Response(ret)

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

def produceRetCode(status = "error", info = "", data = []):
    ret = {}
    ret['status'] = status
    if info:
        ret['info']   = info
    if data:
        ret['data']   = data
    return ret

