from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'labels.views.index', name='index'),  
    url(r'^group/(?P<group_id>\d+)/$', 'labels.views.group', name='group'),
)
