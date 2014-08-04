from backend.personal.common import produceRetCode
from rest_framework.response import Response
from rest_framework import status
from backend.personal.models import UserState

def authenticated(method):
    def wrapper(request, *args):
        try:
            token = request.DATA['token']
            state = UserState.objects.get(token = token)
        except:
            ret = produceRetCode('fail', 'authentication error')
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)
        return method(request, *args)
    return wrapper
