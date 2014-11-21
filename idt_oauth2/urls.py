from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^oauth2/callback/$',
        'oauth2.views.oauth2_callback', name='oauth2_callback'),
    url(r'^oauth2/authorize/(?P<service_name>(\w+))/$',
        'oauth2.views.oauth2_authorize', name='oauth2_authorize'),
)
