from django.conf.urls import patterns, url
from supply import views

urlpatterns = patterns('supply.views',
    # ex: /supply/
    url(r'^$', 'index', name='index'),

    # ex: /supply/orders/new
    url(r'^orders/new/$', 'order_new', name='order_new'),
    # ex: /supply/orders/1/edit
    url(r'^orders/(?P<order_id>\d+)/edit/$', 'order_edit', name='order_edit'),
        
    # ex: /supply/lines
    url(r'^lines/$', 'lines', name='lines'),    
    # ex: /supply/lines/new/order/1
    url(r'^lines/new/order/(?P<order_id>\d+)/$', 'line_new', name='line_new'),
    # ex: /supply/lines/1/edit
    url(r'^lines/(?P<line_id>\d+)/edit/$', 'line_edit', name='line_edit'),

    # ex: /supply/inventory
    url(r'^inventory/$', 'inventory', name='inventory'),
    # ex: /supply/sites/new
    url(r'^sites/new/$', 'site_new', name='site_new'),
    # ex: /supply/sites/1/edit
    url(r'^sites/(?P<site_id>\d+)/edit/$', 'site_edit', name='site_edit'),
    
    # ex: /supply/adunits
    url(r'^adunits/$', 'adunits', name='adunits'),
    # ex: /supply/adunits/new/site/1
    url(r'^adunits/new/site/(?P<site_id>\d+)/$', 'adunit_new', name='adunit_new'),
    # ex: /supply/adunits/1/edit
    url(r'^adunits/(?P<adunit_id>\d+)/edit/$', 'adunit_edit', name='adunit_edit'),
    
    # ex: /supply/reports
    url(r'^reports/$', 'reports', name='reports'),
    # ex: /supply/reports/sites
    url(r'^reports/sites$', 'reports_sites', name='reports_sites'),
    # ex: /supply/reports/1
    url(r'^reports/(?P<report_id>\d+)/$', 'report_detail', name='report_detail'),
)
