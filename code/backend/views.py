#!/usr/bin/env python
# coding: utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS

def index(request):
    return render_to_response('index.html',context_instance=RequestContext(request))

