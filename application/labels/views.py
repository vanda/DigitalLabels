# Create your views here.
from django.http import HttpResponse

def group(request):
    
    return HttpResponse('bar')
    
def index(request):
    
    return HttpResponse('foo')
        