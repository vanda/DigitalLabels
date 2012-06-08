from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'labels.views.index', name='index'),
    url(r'^digitallabel/(?P<digitallabel_id>\d+)/$',
                            'labels.views.digitallabel', name='digitallabel'),
)
