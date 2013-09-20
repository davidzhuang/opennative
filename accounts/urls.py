from django.conf.urls import patterns, url
from supply import views

urlpatterns = patterns('accounts.views',
    # ex: /accounts/
    #url(r'^$', 'index', name='index'),
    # ex: /accounts/signin
    url(r'^signin/$', 'signin', name='signin'),

    # ex: /accounts/error
    url(r'^error/(?P<type>\w+)/$', 'error', name='error'),
)