from backend.calendarr.models import EventItem
from backend.calendarr.serializers import EventSerializer
from backend.personal.models import User, UserState
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.personal.views import produceRetCode, authenticated

@api_view(['POST'])
@authenticated
def addEvent(request):
    request.DATA['user'] = request.DATA['user'].id
    serializer = EventSerializer(data=request.DATA)
    if serializer.is_valid():
    	serializer.save()
    	ret = produceRetCode('success')
    	return Response(ret)
    ret = produceRetCode('fail', 'event info error')
    return Response(ret)

@api_view(['GET'])
@authenticated
def getEventsInRange(request):
    events = EventItem.objects.filter(user = request.DATA['user'])
    try:
        left = request.DATA['left']
        events = events.filter(startdatetime__gte = left)
    except KeyError:
        pass
    try:
        right = request.DATA['right']
        events = events.filter(startdatetime__lte = right)
    except KeyError:
        pass

    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
@authenticated
def alterEvent(request):
    request.DATA['user'] = request.DATA['user'].id
    try:
        event = EventItem.objects.get(id=request.DATA['id'])
    except Exception:
        ret = produceRetCode('fail', 'event does not exist')
        return Response(ret)
    if event.user.id == request.DATA['user']:
        pass
    else:
        ret = produceRetCode('fail', 'permission denied')
        return Response(ret)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = EventSerializer(event, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            ret = produceRetCode('fail', 'event info error')
            return Response(ret)

    if request.method == 'DELETE':
        event.delete()
        ret = produceRetCode('success')
        return Response(ret)


