from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404

def signin(request):
    return render(request, "supply/signin.html", {})

def index(request):
    return render(request, "supply/index.html", {})

def order_new(request):
    return render(request, "supply/order_new.html", {})

def order_edit(request, order_id):
    return render(request, "supply/order_edit.html", {})
    
def lines(request):
    return render(request, "supply/lines.html", {})

def line_new(request, order_id):
    return render(request, "supply/line_new.html", {})
    
def line_edit(request, line_id):
    return render(request, "supply/line_edit.html", {})
    
def inventory(request):
    return render(request, "supply/inventory.html", {})

def site_new(request):
    return render(request, "supply/site_new.html", {})

def site_edit(request, site_id):
    return render(request, "supply/site_edit.html", {})

def adunits(request):
    return render(request, "supply/adunits.html", {})
        
def adunit_new(request, site_id):
    return render(request, "supply/adunit_new.html", {})

def adunit_edit(request, adunit_id):
    return render(request, "supply/adunit_edit.html", {})

def reports(request):
    return render(request, "supply/reports.html", {})

def reports_sites(request):
    return render(request, "supply/reports_sites.html", {})

def report_detail(request, report_id):
    return render(request, "supply/report_detail.html", {})
