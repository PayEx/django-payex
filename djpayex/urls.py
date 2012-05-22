from django.conf.urls.defaults import *

urlpatterns = patterns('djpayex.views',
    url(r'^callback/$', 'callback', name='payex-callback'),
)
