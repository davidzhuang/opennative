from django.conf.urls import patterns, url
from supply import views

urlpatterns = patterns('accounts.views',
    # ex: /accounts/
    #url(r'^$', 'index', name='index'),
    # ex: /accounts/signin
    url(r'^signin/$', 'signin', name='signin'),
    # ex: /accounts/signup
    url(r'^signup/$', 'signup', name='signup'),
    # ex: /accounts/signup_done
    url(r'^signup_done/$', 'signup_done', name='signup_done'),

    # ex: /accounts/error
    url(r'^error/(?P<type>\w+)/$', 'error', name='error'),
)
