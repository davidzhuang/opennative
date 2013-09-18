from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django import forms
from supply.models import *
from supply.forms import site_form

def signin(request):
    return render(request, "supply/signin.html", {})

def index(request):
    all_orders = Order.objects.all()
    return render(request, "supply/index.html", {'order_collection': all_orders})

def order_new(request):
    if request.method == 'POST':
        print 'post\n'
        name_entry=request.POST.get('inputOrderName')
        company_entry=request.POST.get('inputCompany')
        print 'name is: %s \n' % name_entry
        print 'company is: %s \n' % company_entry
        	     
        if ( name_entry and company_entry):
            order = Order()
            order.name = name_entry
            order.company= company_entry
            order.status = 'DFT'
            current_user = User.objects.get(pk=1)
            order.creator = current_user
            order.pub = current_user.pub 
            
            order.save();             
            return HttpResponseRedirect(reverse('supply:inventory'))
        else:
            print 'invalid POST input\n'
            err_invalid_new_order_input = 'invalid new order input'  
            return render(request, 'supply/order_new.html', {'errors':err_invalid_new_order_input, 'name':name_entry, 'company':company_entry})
    else:
        return render(request, 'supply/order_new.html', {})       

def order_edit(request, order_id):
    print 'order_edit: order_id is: %s\n'%order_id
     
    order_to_edit = Order.objects.get(id=order_id)
    
    print 'order_edit: order retrieved is: %s\n'%order_to_edit
    
    if request.method == 'POST':
        print 'order_edit: post\n'
        name_entry=request.POST.get('inputOrderName')
        company_entry=request.POST.get('inputCompany')
        print 'name is: %s \n' % name_entry
        print 'company is: %s \n' % company_entry
        	     
        if ( name_entry and company_entry):
            order_to_edit.name = name_entry
            order_to_edit.company= company_entry
                        
            order_to_edit.save();             
            return HttpResponseRedirect(reverse('supply:index'))
        else:
            print 'invalid POST input\n'
            err_invalid_new_order_input = 'Invalid order editing'  
            return render(request, 'supply/order_edit.html', {'errors':err_invalid_new_order_input, 'name':name_entry, 'company':company_entry})
    else:
        print 'order_edit: HTTP %s method \n'%request.method
        print 'order_edit: HTTP GET, id is: %s\n'%order_id
        print 'order_edit: HTTP GET, name is: %s\n'%order_to_edit.name
        print 'order_edit: HTTP GET, company is: %s\n'%order_to_edit.company
        return render(request, 'supply/order_edit.html', {'id':order_id, 'name':order_to_edit.name, 'company':order_to_edit.company})       
    
def lines(request):
    all_order_items = Order.objects.all()
    all_line_items = LineItem.objects.all()
    print '\n retrieved all orders and all lines from database\n'
    print '\n all orders:\n', all_order_items
    print '\n all line itmes:\n', all_line_items
     
    order_list = []
    line_item_list_by_order = []
    
    for order in all_order_items:
        line_item_list = []
        print '_______________________________'
        print 'order is %s\n'% order
        for line_item in all_line_items:
            if line_item.order == order:
                line_item_list.append(line_item)
                
                #add order to order list if it has line items, and that it is the first line item
                if len(line_item_list) == 1:
                    order_list.append(order)
        print 'line item list built for order %s:\n'%order
        print line_item_list
        if len(line_item_list) > 0:        
            line_item_list_by_order.append(line_item_list)
        print '_______________________________'    
    print 'line item list by order:\n'
    print line_item_list_by_order
    print 'order list:\n'
    print order_list     
        
    return render(request, "supply/lines.html", {'all_orders':order_list, 'line_item_list_by_order': line_item_list_by_order})
    
def line_new(request, order_id):
    return render(request, "supply/line_new.html", {})

def line_edit(request, line_id):
    return render(request, "supply/line_edit.html", {})
    
def inventory(request):
    all_sites = Site.objects.all()
    print '\n retrieved all site data,trying to print\n'
    for item in all_sites:
        print item 
    return render(request, "supply/inventory.html", {'site_collection': all_sites})

def site_new(request):
    print 'enter site_new\n'

    if request.method == 'POST':
        print 'site_new: post\n'

        form = site_form(request.POST)
        if form.is_valid():
            cleaned_form = form.cleaned_data
            print 'name is: %s \n' % cleaned_form['site_name']
            print 'URL is: %s \n' % cleaned_form['site_URL']

            site_model = Site()
            
            site_model.name = cleaned_form['site_name']
            site_model.url = cleaned_form['site_URL']
            site_model.pub = Publisher.objects.get(pk=1)
            site_model.category = "hard_coded"
            
            site_model.save()
            
            return HttpResponseRedirect('/supply/inventory/')
            
        elif form.errors:
            print 'POST form error %s' %form.errors
            
            return render(request, 'supply/site_new.html', {'form': form})    #form.errors accessed in view.py        
    else:
    	print 'site_new: not valid POST request, going back to site_new page\n'
        return render(request, 'supply/site_new.html') 
        
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
