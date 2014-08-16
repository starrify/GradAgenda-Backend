from backend.friend.models import FriendRelation, FriendRequest
from backend.friend.serializers import RelationSerializer, RequestSerializer
from backend.personal.models import User, UserState
from backend.personal.serializers import RegisterSerializer, UserSerializer
from backend.univinfo.models import University, Major, Course, Section
from backend.univinfo.serializers import SectionSerializer, CourseSerializer
from backend.curriculum.models import CourseItem
from backend.curriculum.serializers import CourseItemSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.personal.views import produceRetCode, authenticated

@api_view(['POST'])
@authenticated
def searchForUser(request):
	try:
		query = request.DATA['query']
	except Exception:
		ret = produceRetCode('fail', 'query required')
		return Response(ret, status=status.HTTP_202_ACCEPTED)

	userlist1 = User.objects.filter(email__iexact=query).exclude(id=request.DATA['user'].id)
	userlist2 = User.objects.filter(nick_name__iexact=query).exclude(id=request.DATA['user'].id)
	userlist3 = User.objects.filter(first_name__iexact=query).exclude(id=request.DATA['user'].id)
	userlist4 = User.objects.filter(last_name__iexact=query).exclude(id=request.DATA['user'].id)
	userlist5 = User.objects.filter(gender__iexact=query).exclude(id=request.DATA['user'].id)
	userlist6 = User.objects.filter(phone__iexact=query).exclude(id=request.DATA['user'].id)
	userlist = userlist1 | userlist2 | userlist3 | userlist4 | userlist5 | userlist6
	serializers = UserSerializer(userlist, many=True)
	ret = produceRetCode('success', '', serializers.data)
	return Response(ret, status=status.HTTP_200_OK)

@api_view(['POST'])
@authenticated
def sendFriendRequest(request):
	try:
		receiverid = request.DATA['receiverid']
	except Exception:
		ret = produceRetCode('fail', 'receiverid required')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	try:
		receiver = User.objects.get(id=receiverid)
	except User.DoesNotExist:
		ret = produceRetCode('fail', 'receiver does not exist')
		return Response(ret, status=status.HTTP_202_ACCEPTED)

	data = {}
	data['sender'] = request.DATA['user'].id
	data['receiver'] = receiver.id

	if data['receiver'] == data['sender']:
		ret = produceRetCode('fail', 'receiver should not be the same as sender')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	fr = FriendRequest.objects.filter(sender=data['sender']).filter(receiver=data['receiver'])
	try:
		fr[0]
		ret = produceRetCode('fail', 'request already exist')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	except IndexError:
		pass
	fr = FriendRelation.objects.filter(user1=data['sender']).filter(user2=data['receiver'])
	try:
		fr[0]
		ret = produceRetCode('fail', 'friend already')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	except IndexError:
		pass
	fr = FriendRelation.objects.filter(user1=data['sender']).filter(user2=data['receiver'])
	try:
		fr[0]
		ret = produceRetCode('fail', 'friend already')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	except IndexError:
		pass


	serializer = RequestSerializer(data=data)
	if serializer.is_valid():
		serializer.save()
		ret = produceRetCode('success')
		return Response(ret, status=status.HTTP_200_OK)
	else:
		ret = produceRetCode('fail', 'request format error')
		return Response(ret, status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
@authenticated
def getFriendRequest(request):
	senderlist = FriendRequest.objects.filter(receiver=request.DATA['user'].id)
	serializer = RequestSerializer(senderlist, many=True)
	ret = produceRetCode('success', '', serializer.data)
	return Response(ret, status=status.HTTP_200_OK)


@api_view(['POST'])
@authenticated
def acceptFriendRequest(request):
	try:
		requestid = request.DATA['requestid']
	except Exception:
		ret = produceRetCode('fail', 'request id required')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	try:
		fr = FriendRequest.objects.get(id = requestid)
	except FriendRequest.DoesNotExist:
		ret = produceRetCode('fail', 'request does not exist')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	if fr.receiver.id != request.DATA['user'].id:
		ret = produceRetCode('fail', 'permission denied')
		return Response(ret, status=status.HTTP_202_ACCEPTED)

	data = {}
	data['user1'] = request.DATA['user'].id
	data['user2'] = fr.sender.id
	frelation = FriendRelation.objects.filter(user1=data['user1']).filter(user2=data['user2'])
	try:
		frelation[0]
		ret = produceRetCode('fail', 'friend already')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	except IndexError:
		pass
	frelation = FriendRelation.objects.filter(user2=data['user1']).filter(user1=data['user2'])
	try:
		frelation[0]
		ret = produceRetCode('fail', 'friend already')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	except IndexError:
		pass

	serializer = RelationSerializer(data=data)
	if serializer.is_valid():
		serializer.save()
		fr.delete()
		ret = produceRetCode('success')
		return Response(ret, status=status.HTTP_200_OK)
	else:
		ret = produceRetCode('fail', 'friend relation format error')
		return Response(ret, status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
@authenticated
def rejectFriendRequest(request):
	try:
		requestid = request.DATA['requestid']
	except Exception:
		ret = produceRetCode('fail', 'request id required')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	try:
		fr = FriendRequest.objects.get(id = requestid)
	except FriendRequest.DoesNotExist:
		ret = produceRetCode('fail', 'request does not exist')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	if fr.receiver.id != request.DATA['user'].id:
		ret = produceRetCode('fail', 'permission denied')
		return Response(ret, status=status.HTTP_202_ACCEPTED)

	fr.delete()
	ret = produceRetCode('success')
	return Response(ret, status=status.HTTP_200_OK)

@api_view(['POST'])
@authenticated
def getFriendList(request):
	data = []
	tmp = {}
	friendlist1 = FriendRelation.objects.filter(user1=request.DATA['user'].id)
	friendlist2 = FriendRelation.objects.filter(user2=request.DATA['user'].id)
	friendlist = friendlist1 | friendlist2
	serializer = RelationSerializer(friendlist, many=True)
	ret = produceRetCode('success', '', serializer.data)
	return Response(ret, status=status.HTTP_200_OK)

@api_view(['POST'])
def isFriend(request):
	try:
		user1 = request.DATA['user1']
		user2 = request.DATA['user2']
	except Exception:
		ret = produceRetCode('fail', 'input data format error')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	fr1 = FriendRelation.objects.filter(user1=user1).filter(user2=user2)
	fr2 = FriendRelation.objects.filter(user2=user1).filter(user1=user2)
	fr = fr1 | fr2
	if fr:
		ret = produceRetCode('success', '', 'True')
		return Response(ret, status.HTTP_200_OK)
	else:
		ret = produceRetCode('success', '', 'False')
		return Response(ret, status.HTTP_200_OK)

@api_view(['POST'])
@authenticated
def deleteFriend(request):
	try:
		friendid = request.DATA['friendid']
	except KeyError:
		ret = produceRetCode('fail', 'friend id required')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
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
		return Response(ret, status=status.HTTP_204_NO_CONTENT)
	else:
		ret = produceRetCode('fail', 'not friend yet')
		return Response(ret, status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
@authenticated
def getSameCourses(request):
	try:
		friendid = request.DATA['friendid']
	except KeyError:
		ret = produceRetCode('fail', 'friend id required')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	friendcourses = CourseItem.objects.filter(user=friendid)
	fserializer = CourseItemSerializer(friendcourses, many=True)
	mycourses = CourseItem.objects.filter(user=request.DATA['user'].id)
	mserializer = CourseItemSerializer(mycourses, many=True)
	sections = []
	for friendcourse in fserializer.data:
		for mycourse in mserializer.data:
			if friendcourse["section"] == mycourse["section"]:
				sections.append(friendcourse["section"])
	courseinfo = []
	for section in sections:
		try:
			tsec = Section.objects.get(id=section)
		except Section.DoesNotExist:
			ret = produceRetCode('fail', 'database inconsistance')
			return Response(ret, status=status.HTTP_202_ACCEPTED)
		sserializer = SectionSerializer(tsec)
		try:
			tcourse = Course.objects.get(id=sserializer.data["course"])
		except Course.DoesNotExist:
			ret = produceRetCode('fail', 'database inconsistance')
			return Response(ret, status=status.HTTP_202_ACCEPTED)
		cserializer = CourseSerializer(tcourse)
		courseinfo.append(cserializer.data)
	ret = produceRetCode('success', '', courseinfo)
	return Response(ret, status=status.HTTP_200_OK)

@api_view(['POST'])
def getUsersInfo(request):
	try:
		ids = request.DATA['ids']
	except KeyError:
		ret = produceRetCode('fail', 'user id required')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	users = []
	for pk in ids:
		try:
			user = User.objects.get(id=pk)
		except User.DoesNotExist:
			ret = produceRetCode('fail', 'database inconsistance')
			return Response(ret, status=status.HTTP_202_ACCEPTED)
		userializer = UserSerializer(user)
		users.append(userializer.data)
	ret = produceRetCode('success', '', users)
	return Response(ret, status=status.HTTP_200_OK)

@api_view(['POST'])
def getSameCourseUsers(request):
	try:
		courseid = request.DATA['courseid']
	except KeyError:
		ret = produceRetCode('fail', 'course id required')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	sections = Section.objects.filter(course=courseid)
	sserializer = SectionSerializer(sections, many=True)
	sdata = sserializer.data
	users = []
	for section in sdata:
		courseitems = CourseItem.objects.filter(section=section["id"])
		ciserializer = CourseItemSerializer(courseitems, many=True)
		cidata = ciserializer.data
		for ci in cidata:
			if ci["user"] in users:
				pass
			else:
				users.append(ci["user"])
	ret = produceRetCode('success', '', users)
	return Response(ret, status=status.HTTP_200_OK)


	