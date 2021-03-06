# Create your views here.
from django.http import HttpResponse
from django.template import loader, RequestContext
from labels.models import DigitalLabel, Portal
from django.conf import settings


if hasattr(settings, "KIOSK_MODE"):
    KIOSK_MODE = settings.KIOSK_MODE
else:
    KIOSK_MODE = False

def digitallabel(request, digitallabel_id, objectid=None, pos=None):
    dl = DigitalLabel.objects.get(id=digitallabel_id)
    dlobjects = dl.digitallabelobject_set.all().order_by('position')
    if objectid is not None:
        objectid = int(objectid)
    if pos is not None:
        pos = int(pos)
    t = loader.get_template('digitallabel.html')
    c = RequestContext(request, {'dlobjects': dlobjects, 'screen': dl,
                                 'objectid': objectid, 'pos': pos,
                                 'kiosk_mode': KIOSK_MODE})
    return HttpResponse(t.render(c))


def portal(request, portal_id, objectid=None, labelid=None, pos=None):
    pt = Portal.objects.get(id=portal_id)
    ptlabels = pt.portaltextlabel_set.all().order_by('position')
    ptobjects = pt.portalobject_set.all().order_by('position')
    if objectid is not None:
        objectid = int(objectid)
    if labelid is not None:
        labelid = int(labelid)
    if pos is not None:
        pos = int(pos)
    t = loader.get_template('portal.html')
    c = RequestContext(request, {'ptlabels': ptlabels, 'ptobjects': ptobjects,
                                 'screen': pt, 'labelid': labelid,
                                 'objectid': objectid, 'pos': pos,
                                 'kiosk_mode': KIOSK_MODE})
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
