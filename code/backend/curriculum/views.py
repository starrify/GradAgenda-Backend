from backend.personal.models import User, UserState
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.personal.views import produceRetCode, authenticated
from backend.utils.fetch.fetch import fetch_curriculum
#from backend.univinfo.models import Professor, Course, Section, Lecture
#from backend.univinfo.serializers import ProfessorSerializer, CourseSerializer, SectionSerializer, LectureSerializer
from backend.curriculum.models import CourseItem
from backend.curriculum.serializers import CourseItemSerializer
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

#reviews


