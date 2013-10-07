from django.conf.urls import patterns, url
from supply import views

urlpatterns = patterns('accounts.views',
    # ex: /accounts/
    #url(r'^$', 'index', name='index'),
    # ex: /accounts/signin
    url(r'^signin/$', 'signin', name='signin'),
    # ex: /accounts/signin
    url(r'^signedout/$', 'signedout', name='signedout'),
    # ex: /accounts/signup
    url(r'^signup/$', 'signup', name='signup'),
2yy    # ex: /accounts/signup_done
    url(r'^signup_done/$', 'signup_done', name='signup_done'),
    # ex: /accounts/account_recovery
    url(r'^account_recovery/$', 'account_recovery', name='account_recovery'),
    # ex: /accounts/account_recovery_confirmation
    url(r'^account_recovery_confirmation/$', 'account_recovery_confirmation', name='account_recovery_confirmation'),

    # ex: /accounts/error
    url(r'^error/(?P<type>\w+)/$', 'error', name='error'),

    # ex: /accounts/reset_password_request
    url(r'^reset_password_request/$', 'django.contrib.auth.views.password_reset', name='reset_password_request'),
    # ex: /accounts/password_sent
    url(r'^reset_password_sent/$', 'django.contrib.auth.views.password_reset_done', name='reset_password_done'),
    # ex: /accounts/reset_password_confirm
    url(r'reset_password_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name='reset_password_confirm'),
    # ex: /accounts/reset_password_complete
    url(r'^reset_password_complete/$', 'django.contrib.auth.views.password_reset_complete', name='reset_password_complete'),

)
