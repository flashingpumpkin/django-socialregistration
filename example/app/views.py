from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    if not request.META.get('HTTP_HOST', '') == '127.0.0.1:8000':
        return HttpResponseRedirect('http://127.0.0.1:8000/')
    return render_to_response(
        'index.html', {}, context_instance=RequestContext(request)
    )
