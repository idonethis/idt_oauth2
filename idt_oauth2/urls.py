from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^oauth2/callback/$',
        'idt_oauth2.views.oauth2_callback', name='oauth2_callback'),
    url(r'^oauth2/authorize/(?P<service_name>(\w+))/$',
        'idt_oauth2.views.oauth2_authorize', name='oauth2_authorize'),
)
