# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS

from backend.personal.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from backend.personal.serializers import RegisterSerializer

def register(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            print "mark"
            serializer = RegisterSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data, status=201)
            else:
                return JSONResponse(serializer.errors, status=400)
        except:
            return render_to_response('index.html',context_instance=RequestContext(request))

def show(request):
    users = user.objects.all()
    serializer = RegisterSerializer(users, many=True)
    return JSONResponse(serializer.data)

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)