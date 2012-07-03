from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'labels.views.index', name='index'),
    url(r'^digitallabel/(?P<digitallabel_id>\d+)/$',
                            'labels.views.digitallabel', name='digitallabel'),
    url(r'^digitallabel/(?P<digitallabel_id>\d+)/id/(?P<id>\d+)/$',
                            'labels.views.digitallabel', name='digitallabel'),
    url(r'^digitallabel/(?P<digitallabel_id>\d+)/pos/(?P<pos>\d+)/$',
                            'labels.views.digitallabel', name='digitallabel'),
    url(r'^template/$', 'labels.views.template', name='template'),
)
