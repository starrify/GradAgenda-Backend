from backend.calendarr.models import EventItem
from backend.calendarr.serializers import EventSerializer
from backend.personal.models import User, UserState
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.personal.views import produceRetCode

@api_view(['POST'])
def addevent(request):
	token = request.DATA['token']
	try:
		state = UserState.objects.get(token=token)
	except UserState.DoesNotExist:
		ret = produceRetCode('fail', 'user does not login')
		return Response(ret, status=status.HTTP_400_BAD_REQUEST)
	try:
        user = User.objects.get(id=state.user.id)
        data = {}
        data['user'] = user.id
	except User.DoesNotExist:
		ret = produceRetCode('error', 'database inconsistent')
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)
    try:
    	data['name'] = request.DATA['eventname']
    	data['startdatetime'] = request.DATA['startdatetime']
    	data['enddatetime'] = request.DATA['enddatetime']
    	data['location'] = request.DATA['location']
    	data['status'] = request.DATA['status']
    except KeyError:
    	ret = produceRetCode('error', 'input error')
    	return Response(ret, status=status.HTTP_400_BAD_REQUEST)
    serializer = EventSerializer(data=data)
    if serializer.is_valid():
    	serializer.save()
    	ret = produceRetCode('success')
    	return Response(ret)
    ret = produceRetCode('fail', 'event info error')
    return Response(ret)

    





