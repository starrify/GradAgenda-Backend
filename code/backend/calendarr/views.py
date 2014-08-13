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
    	return Response(ret, status=status.HTTP_201_CREATED)
    ret = produceRetCode('fail', 'event data format error')
    return Response(ret, status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
@authenticated
def getEventList(request):
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
    ret = produceRetCode('success', '', serializer.data)
    return Response(ret, status=status.HTTP_200_OK)

@api_view(['POST'])
@authenticated
def getEvent(request):
    request.DATA['user'] = request.DATA['user'].id
    try:
        eventid = request.DATA['id']
    except KeyError:
        ret = produceRetCode('fail', 'event id required')
        return Response(ret, status=status.HTTP_202_ACCEPTED)
    try:
        event = EventItem.objects.get(id = eventid)
    except EventItem.DoesNotExist:
        ret = produceRetCode('fail', 'event does not exist')
        return Response(ret, status=status.HTTP_202_ACCEPTED)
    if event.user.id == request.DATA['user']:
        pass
    else:
        ret = produceRetCode('fail', 'permission denied')
        return Response(ret, status=status.HTTP_202_ACCEPTED)

    serializer = EventSerializer(event)
    ret = produceRetCode('success', '', serializer.data)
    return Response(ret, status=status.HTTP_200_OK)

@api_view(['POST'])
@authenticated
def alterEvent(request):
    request.DATA['user'] = request.DATA['user'].id
    try:
        eventid = request.DATA['id']
    except KeyError:
        ret = produceRetCode('fail', 'event id required')
        return Response(ret, status=status.HTTP_202_ACCEPTED)
    try:
        event = EventItem.objects.get(id = eventid)
    except EventItem.DoesNotExist:
        ret = produceRetCode('fail', 'event does not exist')
        return Response(ret, status=status.HTTP_202_ACCEPTED)
    if event.user.id == request.DATA['user']:
        pass
    else:
        ret = produceRetCode('fail', 'permission denied')
        return Response(ret, status=status.HTTP_202_ACCEPTED)

    serializer = EventSerializer(event, data=request.DATA)
    if serializer.is_valid():
        serializer.save()
        ret = produceRetCode('success')
        return Response(ret, status=status.HTTP_200_OK)
    else:
        ret = produceRetCode('fail', 'event data format error')
        return Response(ret, status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
@authenticated
def deleteEvent(request):
    request.DATA['user'] = request.DATA['user'].id
    try:
        eventid = request.DATA['id']
    except KeyError:
        ret = produceRetCode('fail', 'event id required')
        return Response(ret, status=status.HTTP_202_ACCEPTED)
    try:
        event = EventItem.objects.get(id = eventid)
    except EventItem.DoesNotExist:
        ret = produceRetCode('fail', 'event does not exist')
        return Response(ret, status=status.HTTP_202_ACCEPTED)
    if event.user.id == request.DATA['user']:
        pass
    else:
        ret = produceRetCode('fail', 'permission denied')
        return Response(ret, status=status.HTTP_202_ACCEPTED)

    event.delete()
    ret = produceRetCode('success')
    return Response(ret, status=status.HTTP_200_OK)


