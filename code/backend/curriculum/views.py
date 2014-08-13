from backend.personal.models import User, UserState
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.personal.views import produceRetCode, authenticated
from backend.utils.fetch.fetch import fetch_curriculum
from backend.univinfo.models import Professor, Section
#from backend.univinfo.serializers import ProfessorSerializer, CourseSerializer, SectionSerializer, LectureSerializer
from backend.curriculum.models import CourseItem, Review
from backend.curriculum.serializers import CourseItemSerializer, ReviewSerializer
import datetime

_data_processor = {}
from backend.utils.process import _UCB
from backend.utils.process import _PU
_data_processor['UCB'] = _UCB
_data_processor['PU'] = _PU


@api_view(['POST'])
@authenticated
def fetchCurriculum(request):
	university = request.DATA['user'].university.shortname
	if university == 'Unknown':
		ret = produceRetCode('fail', 'university not supported')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	try:
		eas_id = request.DATA['eas_id']
		eas_pwd = request.DATA['eas_pwd']
	except KeyError:
		ret = produceRetCode('fail', 'eas id and eas pwd required')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	try:
		semester = request.DATA['semester']
	except KeyError:
		ret = produceRetCode('fail', 'semester required')
		return Response(ret, status=status.HTTP_202_ACCEPTED)

	fetched = fetch_curriculum(university, eas_id, eas_pwd, semester)
	#import pickle
	#with open('data.pickle', 'rb') as f:
	#	fetched = pickle.load(f)
	if fetched['status'] == 'success':
		ret = _data_processor[university].process(fetched['raw-data'], semester, request.DATA['user'])
		return Response(ret, status=status.HTTP_200_OK)
	else:
		ret = produceRetCode('fail', fetched['message'])
		return Response(ret, status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
@authenticated
def getCourseList(request):
	courses = CourseItem.objects.filter(user=request.DATA['user'].id).filter(section__start__lte=datetime.datetime.now()).filter(section__end__gte=datetime.datetime.now())
	serializer = CourseItemSerializer(courses, many=True)
	ret = produceRetCode('success', '', serializer.data)
	return Response(ret, status=status.HTTP_200_OK)

def authreview(method):
	def wrapper(request):
		try:
			rid = request.DATA['rid']
		except KeyError:
			ret = produceRetCode('fail', 'rid required')
			return Response(ret, status=status.HTTP_202_ACCEPTED)
		try:
			review = Review.objects.get(id=rid)
		except Review.DoesNotExist:
			ret = produceRetCode('fail', 'review does not exist')
			return Response(ret, status=status.HTTP_202_ACCEPTED)
		if review.user == request.DATA['user'].id:
			request.DATA['review'] = review
		else:
			ret = produceRetCode('fail', 'permission denied')
			return Response(ret, status=status.HTTP_202_ACCEPTED)
		return method(request)
	return wrapper

@api_view(['POST'])
@authenticated
def setReview(request):
	request.DATA['user'] = request.DATA['user'].id
	serializer = ReviewSerializer(data=request.DATA)
	try:
		is_course = request.DATA['is_course']
	except KeyError:
		ret = produceRetCode('fail', 'is_course flag required')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	if is_course:
		try:
			section = request.DATA['section']
		except KeyError:
			ret = produceRetCode('fail', 'section id required')
			return Response(ret, status=status.HTTP_202_ACCEPTED)
		try:
			section = Section.objects.get(id=section)
		except Section.DoesNotExist:
			ret = produceRetCode('fail', 'section does not exist')
			return Response(ret, status=status.HTTP_202_ACCEPTED)
		try:
			review = Review.objects.get(user=request.DATA['user'], section=section.id)
		except Review.DoesNotExist:
			serializer = ReviewSerializer(data=request.DATA)
			if serializer.is_valid():
				serializer.save()
				try:
					section.rate = (section.rate * section.ratecount + request.DATA['rate']) / (section.ratecount + 1)
					section.ratecount = section.ratecount + 1
					section.save()
				except Exception:
					ret = produceRetCode('fail', 'computing error')
					return Response(ret, status=status.HTTP_202_ACCEPTED)
			else:
				ret = produceRetCode('fail', 'add review data format error')
				return Response(ret, status=status.HTTP_202_ACCEPTED)
		serializer = ReviewSerializer(review, data=request.DATA)
		if serializer.is_valid():
			serializer.save()
			try:
				section.rate = (section.rate * section.ratecount - review.rate + request.DATA['rate']) / section.ratecount
				section.save()
			except Exception:
				ret = produceRetCode('fail', 'rate computing error')
				return Response(ret, status=status.HTTP_202_ACCEPTED)
		else:
				ret = produceRetCode('fail', 'change review data format error')
				return Response(ret, status=status.HTTP_202_ACCEPTED)
	else:
		try:
			professor = request.DATA['professor']
		except KeyError:
			ret = produceRetCode('fail', 'professor id required')
			return Response(ret, status=status.HTTP_202_ACCEPTED)
		try:
			professor = Professor.objects.get(id=professor)
		except Professor.DoesNotExist:
			ret = produceRetCode('fail', 'professor does not exist')
			return Response(ret, status=status.HTTP_202_ACCEPTED)
		try:
			review = Review.objects.get(user=request.DATA['user'], professor=professor.id)
		except Review.DoesNotExist:
			serializer = ReviewSerializer(data=request.DATA)
			if serializer.is_valid():
				serializer.save()
				try:
					professor.rate = (professor.rate * professor.ratecount + request.DATA['rate']) / (professor.ratecount + 1)
					professor.ratecount = professor.ratecount + 1
					professor.save()
				except Exception:
					ret = produceRetCode('fail', 'rate computing error')
					return Response(ret, status=status.HTTP_202_ACCEPTED)
			else:
				ret = produceRetCode('fail', 'review data format error')
				return Response(ret, status=status.HTTP_202_ACCEPTED)
		serializer = ReviewSerializer(review, data=request.DATA)
		if serializer.is_valid():
			serializer.save()
			try:
				professor.rate = (professor.rate * professor.ratecount - review.rate + request.DATA['rate']) / professor.ratecount
				professor.save()
			except Exception:
				ret = produceRetCode('fail', 'rate computing error')
				return Response(ret, status=status.HTTP_202_ACCEPTED)
		else:
				ret = produceRetCode('fail', 'review data format error')
				return Response(ret, status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
@authenticated
@authreview
def getReview(request):
	serializer = ReviewSerializer(data)
	ret = produceRetCode('success', '', serializer.data)
	return Response(ret, status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
@authenticated
@authreview
def alterReview(request):
	serializer = ReviewSerializer(review, data=request.DATA)
	if serializer.is_valid():
		serializer.save()
		ret = produceRetCode('success')
		return Response(ret, status=status.HTTP_200_OK)
	else:
		ret = produceRetCode('fail', 'review data format error')
		return Response(ret, status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
@authenticated
@authreview
def deleteReview(request):
	request.DATA['review'].delete()
	ret = produceRetCode('success')
	return Response(ret, status=status.HTTP_200_OK)


