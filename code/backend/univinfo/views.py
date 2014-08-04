from backend.univinfo.input import inputUniversities, inputMajors
from backend.univinfo.models import University, Major, Course
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.personal.views import produceRetCode, authenticated
# Create your views here.

@api_view(['GET'])
def inputUnivinfo(request):
	inputUniversities()
	inputMajors()
	ret = produceRetCode('success')
	return Response(ret, status=status.HTTP_200_OK)