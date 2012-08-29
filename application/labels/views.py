# Create your views here.
from django.http import HttpResponse
from django.template import loader, RequestContext
from labels.models import DigitalLabel, Portal


def digitallabel(request, digitallabel_id, objectid=None, pos=None):
    dl = DigitalLabel.objects.get(id=digitallabel_id)
    mobjects = dl.museumobjects.all()
    if objectid is not None:
        objectid = int(objectid)
    if pos is not None:
        pos = int(pos)
    t = loader.get_template('digitallabel.html')
    c = RequestContext(request, {'mobjects': mobjects, 'dl': dl,
                                 'objectid': objectid, 'pos': pos})
    return HttpResponse(t.render(c))


def portal(request, portal_id, objectid=None, labelid=None, pos=None):
    pt = Portal.objects.get(id=portal_id)
    tl = pt.textlabels.all()
    mobjects = pt.museumobjects.all()
    if objectid is not None:
        objectid = int(objectid)
    if labelid is not None:
        labelid = int(labelid)
    if pos is not None:
        pos = int(pos)
    t = loader.get_template('portal.html')
    c = RequestContext(request, {'tlabel': tl, 'mobjects': mobjects, 'pt': pt,
                                 'labelid': labelid, 'objectid': objectid, 'pos': pos})
    return HttpResponse(t.render(c))


def index(request):
    """Lists available digital labels"""
    labels = DigitalLabel.objects.all()
    t = loader.get_template('base.html')
    c = RequestContext(request, {'labels': labels})
    return HttpResponse(t.render(c))


def template(request):
    """Preview the layout of fields in the frontend"""
    t = loader.get_template('template.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))
