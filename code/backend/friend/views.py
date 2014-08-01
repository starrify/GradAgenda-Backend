from backend.friend.models import FriendRelation, FriendRequest
from backend.friend.serializers import RelationSerializer, RequestSerializer
from backend.personal.models import User, UserState
from backend.personal.serializers import RegisterSerializer
from backend.univinfo.models import University, Major, Course
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.personal.views import produceRetCode, authenticated

@api_view(['GET'])
def searchForUser(request):
	try:
		query = request.DATA['query']
	except Exception:
		ret = produceRetCode('fail', 'event info error')
		return Response(ret)

	userlist1 = User.objects.filter(email=query)
	userlist2 = User.objects.filter(nick_name=query)
	userlist3 = User.objects.filter(first_name=query)
	userlist4 = User.objects.filter(last_name=query)
	userlist5 = User.objects.filter(gender=query)
	userlist6 = User.objects.filter(phone=query)
	userlist = userlist1 | userlist2 | userlist3 | userlist4 | userlist5 | userlist6
	serializers = RegisterSerializer(userlist, many=True)
	return Response(serializers.data)

@api_view(['POST'])
@authenticated
def sendFriendRequest(request):
	try:
		receiverid = request.DATA['receiverid']
	except Exception:
		ret = produceRetCode('fail', 'receiverid required')
		return Response(ret)
	try:
		receiver = User.objects.get(id=receiverid)
	except User.DoesNotExist:
		ret = produceRetCode('fail', 'receiver does not exist')
		return Response(ret)

	data = {}
	data['sender'] = request.DATA['user'].id
	data['receiver'] = receiver.id

	if data['receiver'] == data['sender']:
		ret = produceRetCode('fail', 'receiver should not be the same as sender')
		return Response(ret)
	fr = FriendRequest.objects.filter(sender=data['sender']).filter(receiver=data['receiver'])
	try:
		fr[0]
		ret = produceRetCode('fail', 'request already exist')
		return Response(ret)
	except IndexError:
		pass
	fr = FriendRelation.objects.filter(user1=data['sender']).filter(user2=data['receiver'])
	try:
		fr[0]
		ret = produceRetCode('fail', 'friend already')
		return Response(ret)
	except IndexError:
		pass
	fr = FriendRelation.objects.filter(user1=data['sender']).filter(user2=data['receiver'])
	try:
		fr[0]
		ret = produceRetCode('fail', 'friend already')
		return Response(ret)
	except IndexError:
		pass


	serializer = RequestSerializer(data=data)
	if serializer.is_valid():
		serializer.save()
		ret = produceRetCode('success')
		return Response(ret)
	else:
		ret = produceRetCode('fail', 'request format error')
		return Response(ret)


@api_view(['GET'])
@authenticated
def getFriendRequest(request):
	senderlist = FriendRequest.objects.filter(receiver=request.DATA['user'].id)
	serializer = RequestSerializer(senderlist, many=True)
	return Response(serializer.data)


@api_view(['POST'])
@authenticated
def acceptFriendRequest(request):
	try:
		requestid = request.DATA['requestid']
	except Exception:
		ret = produceRetCode('fail', 'request id required')
		return Response(ret)
	try:
		fr = FriendRequest.objects.get(id = requestid)
	except FriendRequest.DoesNotExist:
		ret = produceRetCode('fail', 'request does not exist')
		return Response(ret)
	if fr.receiver.id != request.DATA['user'].id:
		ret = produceRetCode('fail', 'permission denied')
		return Response(ret)

	data = {}
	data['user1'] = request.DATA['user'].id
	data['user2'] = fr.sender.id
	frelation = FriendRelation.objects.filter(user1=data['user1']).filter(user2=data['user2'])
	try:
		frelation[0]
		ret = produceRetCode('fail', 'friend already')
		return Response(ret)
	except IndexError:
		pass
	frelation = FriendRelation.objects.filter(user2=data['user1']).filter(user1=data['user2'])
	try:
		frelation[0]
		ret = produceRetCode('fail', 'friend already')
		return Response(ret)
	except IndexError:
		pass

	serializer = RelationSerializer(data=data)
	if serializer.is_valid():
		serializer.save()
		fr.delete()
		ret = produceRetCode('success')
		return Response(ret)
	else:
		ret = produceRetCode('fail', 'friend relation format error')
		return Response(ret)


@api_view(['POST'])
@authenticated
def rejectFriendRequest(request):
	try:
		requestid = request.DATA['requestid']
	except Exception:
		ret = produceRetCode('fail', 'request id required')
		return Response(ret)
	try:
		fr = FriendRequest.objects.get(id = requestid)
	except FriendRequest.DoesNotExist:
		ret = produceRetCode('fail', 'request does not exist')
		return Response(ret)
	if fr.receiver.id != request.DATA['user'].id:
		ret = produceRetCode('fail', 'permission denied')
		return Response(ret)

	fr.delete()
	ret = produceRetCode('success')
	return Response(ret)

@api_view(['GET'])
@authenticated
def getFriendList(request):
	friendlist1 = FriendRelation.objects.filter(user1=request.DATA['user'].id)
	friendlist2 = FriendRelation.objects.filter(user2=request.DATA['user'].id)
	friendlist = friendlist1 | friendlist2
	serializer = RelationSerializer(friendlist, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def isFriend(request):
	try:
		user1 = request.DATA['user1']
		user2 = request.DATA['user2']
	except Exception:
		ret = produceRetCode('fail', 'input data format error')
		return Response(ret)
	fr1 = FriendRelation.objects.filter(user1=user1).filter(user2=user2)
	fr2 = FriendRelation.objects.filter(user2=user1).filter(user1=user2)
	fr = fr1 | fr2
	if fr:
		return Response(True)
	else:
		return Response(False)

@api_view(['POST'])
@authenticated
def deleteFriend(request):
	try:
		friendid = request.DATA['friendid']
	except KeyError:
		ret = produceRetCode('fail', 'friend id required')
		return Response(ret)
	success = False
	fr = FriendRelation.objects.filter(user1 = friendid).filter(user2 = request.DATA['user'].id)
	try:
		fr[0]
		fr.delete()
		success=True
	except IndexError:
		pass
	fr = FriendRelation.objects.filter(user2 = friendid).filter(user1 = request.DATA['user'].id)
	try:
		fr[0]
		fr.delete()
		success=True
	except IndexError:
		pass
	if success:
		ret = produceRetCode('success')
		return Response(ret)
	else:
		ret = produceRetCode('fail', 'not friend yet')
		return Response(ret)


