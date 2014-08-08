from backend.univinfo.input import inputUniversities, inputMajors, inputSemesters
from backend.univinfo.models import University, Major, Semester, Professor, Course, Section, Lecture
from backend.univinfo.serializers import UniversitySerializer, MajorSerializer, SemesterSerializer, ProfessorSerializer, CourseSerializer, SectionSerializer, LectureSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.personal.views import produceRetCode, authenticated

#setting up
@api_view(['GET'])
def inputUnivinfo(request):
	inputUniversities()
	inputMajors()
	inputSemesters()
	ret = produceRetCode('success')
	return Response(ret, status=status.HTTP_200_OK)

@api_view(['GET'])
def getUniversities(request):
	try:
		query = request.DATA['query']
		universities1 = University.objects.filter(fullname__contains=query)
		universities2 = University.objects.filter(shortname__iexact=query)
		universities = universities1 | universities2
	except KeyError:
		universities = University.objects.all()
	serializer = UniversitySerializer(universities, many=True)
	ret = produceRetCode('success', '', serializer.data)
	return Response(ret, status=status.HTTP_200_OK)

@api_view(['GET'])
def getMajors(request):
	try:
		query = request.DATA['query']
		majors1 = Major.objects.filter(fullname__contains=query)
		majors2 = Major.objects.filter(shortname__iexact=query)
		majors = majors1 | majors2
	except KeyError:
		majors = Major.objects.all()
	serializer = MajorSerializer(majors, many=True)
	ret = produceRetCode('success', '', serializer.data)
	return Response(ret, status=status.HTTP_200_OK)

@api_view(['GET'])
def getProfessors(request):
	try:
		query = request.DATA['query']
		professors1 = Professor.objects.filter(first_name__contains=query)
		professors2 = Professor.objects.filter(last_name__contains=query)
		professors = professors1 | professors2
	except KeyError:
		professors = Professor.objects.all()
	serializer = ProfessorSerializer(professors, many=True)
	ret = produceRetCode('success', '', serializer.data)
	return Response(ret, status=status.HTTP_200_OK)

@api_view(['GET'])
def getSemesters(request):
	try:
		university = request.DATA['university']
	except KeyError:
		ret = produceRetCode('fail', 'university shortname required')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	semesters = Semester.objects.filter(university__shortname=university)
	serializer = SemesterSerializer(semesters, many=True)
	ret = produceRetCode('success', '', serializer.data)
	return Response(ret, status=status.HTTP_200_OK)

@api_view(['GET'])
def getCourse(request):
	try:
		sectionid = request.DATA['sectionid']
	except KeyError:
		ret = produceRetCode('fail', 'section id required')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	try:
		section = Section.objects.get(id=sectionid)
	except Section.DoesNotExist:
		ret = produceRetCode('fail', 'section not found')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	course = section.course
	serializer = CourseSerializer(course)
	ret = produceRetCode('success', '', serializer.data)
	return Response(ret, status=status.HTTP_200_OK)

@api_view(['GET'])
def getSection(request):
	try:
		sectionid = request.DATA['sectionid']
	except KeyError:
		ret = produceRetCode('fail', 'section id required')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	try:
		section = Section.objects.get(id=sectionid)
	except Section.DoesNotExist:
		ret = produceRetCode('fail', 'section not found')
		return Response(ret, status=status.HTTP_202_ACCEPTED)

	serializer = SectionSerializer(section)
	ret = produceRetCode('success', '', serializer.data)
	return Response(ret, status=status.HTTP_200_OK)

@api_view(['GET'])
def getLectures(request):
	try:
		sectionid = request.DATA['sectionid']
	except KeyError:
		ret = produceRetCode('fail', 'section id required')
		return Response(ret, status=status.HTTP_202_ACCEPTED)
	lectures = Lecture.objects.filter(section__id=sectionid)
	serializer = LectureSerializer(lectures, many=True)
	ret = produceRetCode('success', '', serializer.data)
	return Response(ret, status=status.HTTP_200_OK)
