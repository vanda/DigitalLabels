from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'labels.views.index', name='index'),
    url(r'^template/$', 'labels.views.template', name='template'),
    #DigitalLabel urls
    url(r'^digitallabel/(?P<digitallabel_id>\d+)/$',
                            'labels.views.digitallabel', name='digitallabel'),
    url(r'^digitallabel/(?P<digitallabel_id>\d+)/objectid/(?P<objectid>\d+)/$',
                            'labels.views.digitallabel', name='digitallabel'),
    url(r'^digitallabel/(?P<digitallabel_id>\d+)/pos/(?P<pos>\d+)/$',
                            'labels.views.digitallabel', name='digitallabel'),
    #Portal urls
    url(r'^portal/(?P<portal_id>\d+)/$',
                            'labels.views.portal', name='portal'),
    url(r'^portal/(?P<portal_id>\d+)/labelid/(?P<labelid>\d+)/$',
                            'labels.views.portal', name='portal'),
    url(r'^portal/(?P<portal_id>\d+)/objectid/(?P<objectid>\d+)/$',
                            'labels.views.portal', name='portal'),
    url(r'^portal/(?P<portal_id>\d+)/pos/(?P<pos>\d+)/$',
                            'labels.views.portal', name='portal'),
)
