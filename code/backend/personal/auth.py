def authenticated(method):
    def wrapper(request, *args):
        try:
            token = request.DATA['token']
            user = User.objects.get(email = email)
            state = UserState.objects.get(token = token)
        except:
            ret = produceRetCode('fail', 'need authenticated')
            print "haha"
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)
        return method(request, *args)
    return wrapper
