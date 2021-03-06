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
        except KeyError:
            ret = produceRetCode('fail', 'token required')
            return Response(ret, status=status.HTTP_202_ACCEPTED)
        try:
            state = UserState.objects.get(token=token)
        except UserState.DoesNotExist:
            ret = produceRetCode('fail', 'user did not login')
            return Response(ret, status=status.HTTP_202_ACCEPTED)
        try:
            user = User.objects.get(id=state.user.id)
        except User.DoesNotExist:
            ret = produceRetCode('error', 'database inconsistent')
            return Response(ret, status=status.HTTP_202_ACCEPTED)
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
            return Response(ret, status=status.HTTP_202_ACCEPTED)

        try:
            user = User.objects.get(email = email)
            ret = produceRetCode('fail', 'email already exist')
            return Response(ret, status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist:
            pass

        try:
            universityname = request.DATA['university']
        except KeyError:
            universityname = 'Unknown'
        try:
            university = University.objects.get(shortname__iexact = universityname)
        except University.DoesNotExist:
            university = University.objects.get(shortname = "Unknown")

        try:
            majorname = request.DATA['major']
        except KeyError:
            majorname = 'Unknown'
        try:
            major = Major.objects.get(shortname__iexact = majorname)
        except University.DoesNotExist:
            major = Major.objects.get(shortname = "Unknown")

        request.DATA['university'] = university.id
        request.DATA['major'] = major.id
        serializer = RegisterSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            ret = produceRetCode('success', '', serializer.data)
            return Response(ret, status=status.HTTP_200_OK)
        else:
            ret = produceRetCode('fail', 'register data format error', request.DATA)
            return Response(ret, status=status.HTTP_202_ACCEPTED)
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
        return Response(ret, status=status.HTTP_202_ACCEPTED)
    try:
        user = User.objects.get(email = email)
    except User.DoesNotExist:
        ret = produceRetCode('fail', 'user did not register')
        return Response(ret, status=status.HTTP_202_ACCEPTED)
    if request.DATA['password'] == user.password:
        ip = getIP(request)
        token = produceLoginToken(user.id)
        return setUserState(user, ip, token)
    else:
        ret = produceRetCode('fail','invalid email or password')
        return Response(ret, status=status.HTTP_202_ACCEPTED)


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
    return Response(ret, status=status.HTTP_200_OK)

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
            return Response(ret, status=status.HTTP_202_ACCEPTED)
    except KeyError:
        ret = produceRetCode("fail", "password required")
        return Response(ret, status=status.HTTP_202_ACCEPTED)
    try:
        if user.email == request.DATA['email']:
            pass
        else:
            ret = produceRetCode("fail", "email can not be changed")
            return Response(ret, status=status.HTTP_202_ACCEPTED)
    except KeyError:
        ret = produceRetCode("fail", "email required")
        return Response(ret, status=status.HTTP_202_ACCEPTED)
    try:
        universityname = request.DATA['university']
    except KeyError:
        universityname = 'Unknown'
    try:
        university = University.objects.get(shortname__iexact = universityname)
    except University.DoesNotExist:
        university = University.objects.get(shortname = "Unknown")

    try:
        majorname = request.DATA['major']
    except KeyError:
        majorname = 'Unknown'
    try:
        major = Major.objects.get(shortname__iexact = majorname)
    except Major.DoesNotExist:
        major = Major.objects.get(shortname = "Unknown")

    request.DATA['university'] = university.id
    request.DATA['major'] = major.id

    serializer = RegisterSerializer(user, data = request.DATA)
    if serializer.is_valid():
        serializer.save()
        ret = produceRetCode('success')
        return Response(ret, status=status.HTTP_200_OK)
    else:
        ret = produceRetCode('fail', 'user data format error')
        return Response(ret, status=status.HTTP_202_ACCEPTED)


"""
upload pictures:

"""
@api_view(['POST'])
@authenticated
def uploadPic(request):
    user = request.DATA['user']
    user.image = request.FILES['docfile']
    user.save()
    ret = produceRetCode('success', user.image.url)
    return Response(ret, status=status.HTTP_202_ACCEPTED)

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
        return Response(ret, status=status.HTTP_202_ACCEPTED)


"""
import for facebook OAuth
"""
import urllib
import urllib2
from facebook import FacebookAPI, GraphAPI

APP_ID = "1518316575054188"
APP_SECRET = "2b19131660edda56deece972bc4c5aef"
uri = "http://testinglife.duapp.com/login/"

@api_view(['POST'])
def login_facebook(request):
    try:
        code = request.DATA['code']
    except KeyError:
        ret = produceRetCode("fail", "code required")
        return Response(ret, status=status.HTTP_202_ACCEPTED)
    try:
        f = FacebookAPI(APP_ID, APP_SECRET, uri)
        res = f.get_access_token(code) # get long term token
        graph = GraphAPI(res['access_token'])  # access GraphAPI of facebook
        personalInfo = graph.get('me')
    except Exception:
        ret = produceRetCode("fail", "facebook api error")
        return Response(ret, status=status.HTTP_202_ACCEPTED)
    university = University.objects.get(shortname = "Unknown")
    major      = Major.objects.get(shortname = "Unknown")

    userData = {
        "first_name": personalInfo['first_name'],
        "last_name" : personalInfo['last_name'],
        "nick_name" : personalInfo['name'],
        "password"  : "Unknown",
        "gender"    : personalInfo['gender'],
        "image"     : "Unknown",
        "tpa_type"  : "facebook",
        "tpa_id"    : "facebook" + personalInfo['id'],
        "tpa_token" : res['access_token'],
        "university": university.id,  # default university id
        "major"     : major.id,
        "email"     : "Unknown@test.com",
        "phone"     : "Unknown"
    }
    try:
        user  = User.objects.get(tpa_id=userData['tpa_id'])
        # user account exist, directly login
        token = produceLoginToken(userData['tpa_id'])
        ip    = getIP(request)
        return setUserState(user.id, ip, token)
    except User.DoesNotExist:  # create new account
        serializer = RegisterSerializer(data=userData)
        if serializer.is_valid():
            serializer.save()
            user  = User.objects.get(tpa_id=userData['tpa_id'])
            token = produceLoginToken(userData['tpa_id'])
            ip    = getIP(request)
            return setUserState(user.id, ip, token)
        else:
            ret = produceRetCode('fail', 'login data from facebook error', serializer.errors)
            return Response(ret, status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
@authenticated
def userInfo(request):
    user = request.DATA['user']
    userData = {
        "first_name": user.first_name,
        "last_name" : user.last_name,
        "nick_name" : user.nick_name,
        "gender"    : user.gender,
        "image"     : user.image,
        "tpa_type"  : user.tpa_type,
        "tpa_id"    : user.tpa_id,
        "tpa_token" : user.tpa_token,
        "university": user.university.id,
        "major"     : user.major.id,
        "email"     : user.email,
        "phone"     : user.phone
    }
    ret = produceRetCode('success', '', userData)
    return Response(ret, status=status.HTTP_200_OK)


def getIP(request):
    ip = "0.0.0.0"
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip

def setUserState(user, ip, token):
    user_id = user.id
    stateData = {}
    stateData['user']  = user_id
    stateData['token'] = token
    stateData['ip']    = ip
    serializer = UserStateSerializer(data=stateData)
    if serializer.is_valid():
        serializer.save()
        stateData["first_name"]= user.first_name
        stateData["last_name"] = user.last_name
        stateData["nick_name"] = user.nick_name
        stateData["gender"]    = user.gender
        stateData["image"]     = user.image
        stateData["tpa_type"]  = user.tpa_type
        stateData["tpa_id"]    = user.tpa_id
        stateData["tpa_token"] = user.tpa_token
        stateData["university"]= user.university.id
        stateData["major"]     = user.major.id
        stateData["email"]     = user.email
        stateData["phone"]     = user.phone
        ret = produceRetCode('success','',stateData)
        return Response(ret, status=status.HTTP_200_OK)
    else:
        ret = produceRetCode('error', 'invalid UserState data')
        return Response(ret, status=status.HTTP_202_ACCEPTED)

def produceLoginToken(userID):
    userID = str(userID)
    m = hashlib.md5()
    m.update(userID)
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
    return token

def produceRetCode(status = "error", message = "", data = []):
    ret = {}
    ret['status'] = status
    if message:
        ret['message']   = message
    if data:
        ret['data']   = data
    return ret
