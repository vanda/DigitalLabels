# Create your views here.
from django.http import HttpResponse
from django.template import loader, RequestContext
from labels.models import DigitalLabel


def digitallabel(request, digitallabel_id):

    dl = DigitalLabel.objects.get(id=digitallabel_id)
    mobjects = dl.museumobjects.all()

    t = loader.get_template('digitallabel.html')
    c = RequestContext(request, {'mobjects': mobjects})

    return HttpResponse(t.render(c))


def index(request):
    """Lists available digital labels"""
    labels = DigitalLabel.objects.all()
    t = loader.get_template('base.html')
    c = RequestContext(request, {'labels': labels})
    return HttpResponse(t.render(c))
