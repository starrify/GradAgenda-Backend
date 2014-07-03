# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS

from backend.personal.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from backend.personal.serializers import RegisterSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def register(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        users = User.objects.all()
        serializer = RegisterSerializer(users, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def login(request):
    user_name = request.DATA['nick_name']
    user = User.objects.get(nick_name = user_name)

    if request.DATA['password'] == user.password:
        ret = produceRetCode('success')
    else:
        ret = produceRetCode('fail','user_name or password error')
    return Response(ret)

@api_view(['POST'])
def edit(request):
    user_name = request.DATA['nick_name']
    try:
        user = User.objects.get(nick_name = user_name)
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

def produceRetCode(status = "error", info = "", data = []):
    ret = {}
    ret['status'] = status
    if info:
        ret['info']   = info
    if data:
        ret['data']   = data
    return ret

