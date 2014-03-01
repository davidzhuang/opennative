from django.conf.urls import patterns, url, include
from supply import views
from django.contrib.auth import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

urlpatterns = patterns('accounts.views',
    # ex: /accounts/
    #url(r'^$', 'index', name='index'),
    # ex: /accounts/signin
    url(r'^signin/$', 'signin', name='signin'),
    # ex: /accounts/signin
    url(r'^signedout/$', 'signedout', name='signedout'),
    # ex: /accounts/signup
    url(r'^signup/$', 'signup', name='signup'),
    # ex: /accounts/signup_done
    url(r'^signup_done/$', 'signup_done', name='signup_done'),
    # ex: /accounts/reset
    url(r'^reset/$', 'reset', name='reset'),
    # ex: /accounts/password_sent
#    url(r'^reset_password_sent/$', 'django.contrib.auth.views.password_reset_done'),
    # ex: /accounts/reset_password_confirm
    url(r'reset_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'reset_confirm', name='reset_confirm'),
    # ex: /accounts/reset_password_complete
#    url(r'^reset_password_complete/$', 'django.contrib.auth.views.password_reset_complete'),

    # ex: /accounts/error
    url(r'^error/(?P<type>\w+)/$', 'error', name='error'),

    #user name autocomplete URL, /accounts/signup/lookup
    url(r'^signup/lookup', 'username_lookup'),
    #end user name autocomplete
    # ex: /accounts/account_recovery
    #url(r'^account_recovery/$', 'account_recovery', name='account_recovery'),
    # ex: /accounts/account_recovery_confirmation
    #url(r'^account_recovery_confirmation/$', 'account_recovery_confirmation', name='account_recovery_confirmation'),


    #Don't remove, this is important!
    #url(r'^account/', include('django.contrib.auth.urls')),
    #this is the accounts app main url
    #url(r'^accounts/', include('accounts.urls', namespace="accounts"))
)
# add password recovery views
#urlpatterns += patterns('accounts.views', url(r'^forgot_password/$', 'forgot_password', name="forgot_password" ),)

#this is the url for password reset authentication
#urlpatterns += patterns('',
    # ex: /accounts/reset_password_request
#    url(r'^reset_password_request/$', 'django.contrib.auth.views.password_reset'),
    # ex: /accounts/password_sent
#    url(r'^reset_password_sent/$', 'django.contrib.auth.views.password_reset_done'),
    # ex: /accounts/reset_password_confirm
#    url(r'reset_password_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    # ex: /accounts/reset_password_complete
#    url(r'^reset_password_complete/$', 'django.contrib.auth.views.password_reset_complete'),

#)
