from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from supply.models import *
from supply.forms import site_form

#python library
from datetime import datetime

@login_required
def index(request):
    all_orders = Order.objects.all()
    return render(request, "supply/index.html", {'order_collection': all_orders})

@login_required
def order_new(request):
    if request.method == 'POST':
        name_entry=request.POST.get('inputOrderName')
        company_entry=request.POST.get('inputCompany')

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
            err_invalid_new_order_input = 'invalid new order input'  
            return render(request, 'supply/order_new.html', {'errors':err_invalid_new_order_input, 'name':name_entry, 'company':company_entry})
    else:
        return render(request, 'supply/order_new.html', {})       

@login_required
def order_edit(request, order_id):
     
    order_to_edit = Order.objects.get(id=order_id)
    
    if request.method == 'POST':
        name_entry=request.POST.get('inputOrderName')
        company_entry=request.POST.get('inputCompany')
        	     
        if ( name_entry and company_entry):
            order_to_edit.name = name_entry
            order_to_edit.company= company_entry
                        
            order_to_edit.save();             
            return HttpResponseRedirect(reverse('supply:index'))
        else:
            err_invalid_new_order_input = 'Invalid order editing'  
            return render(request, 'supply/order_edit.html', {'errors':err_invalid_new_order_input, 'name':name_entry, 'company':company_entry})
    else:
        return render(request, 'supply/order_edit.html', {'id':order_id, 'name':order_to_edit.name, 'company':order_to_edit.company})       
    
@login_required
def lines(request):
    class all_lines_by_order:
        line_item_list = []
        one_order = None   
    
    all_orders_with_line_items = []

    all_order_items = Order.objects.all()
    all_line_items = LineItem.objects.all()
    
    for order in all_order_items:
        line_item_list = []
        
        for line_item in all_line_items:
            if line_item.order == order:
                line_item_list.append(line_item)
                
                #add order to order list if it has line items, and that it is the first line item
                if len(line_item_list) == 1:
                    one_combined_entry = all_lines_by_order()
                    one_combined_entry.order = order
                    
        if len(line_item_list) > 0:
          one_combined_entry.line_item_list = line_item_list                     
          all_orders_with_line_items.append(one_combined_entry)

    return render(request, "supply/lines.html", {'all_orders_with_line_items':all_orders_with_line_items})
    
@login_required
def line_new(request, order_id):
    if request.method == 'POST':
        name_entry = request.POST.get('inputLineName')
        platform_entry = request.POST.get('platform');
        type_entry = request.POST.get('type')
        adUnit_name_entry = request.POST.get('inventory')
        
        print request.POST
        
        AdUnit_list=[]
        
#        for item in request.POST.get('inventory')
#            adUnit_list.append(item)     
#           print item
        
        print 'name_entry: %s'%name_entry
        print 'platform_entry: %s'%platform_entry
        print 'type_entry: %s'%type_entry
        print 'adUnit_name_entry: %s'%adUnit_name_entry

        if ( name_entry and platform_entry and type_entry and adUnit_name_entry):
			#lineItem table
            new_line_item = LineItem()
            new_line_item.name = name_entry
            new_line_item.platform = platform_entry
            new_line_item.order= Order.objects.get(id = order_id)
            new_line_item.type = type_entry
            
            #non-mandatory attributes 
            new_line_item.status = 'W'
            new_line_item.start_date = datetime.today().isoformat()
            new_line_item.start_time = datetime.now().time().isoformat()
    end_date = models.DateField()
    end_time = models.TimeField()
            #retrieve selected adUnits            
             
            new_line_item.save(); 
            
            #lineItemAdUnit table
#            for item in adUnit_list:
#               new_line_item_adUnit = LineItemAdUnit()
                
#                new_line_item_adUnit.line = new_line_item
#                new_line_item_adUnit.unit = item
                
#               new_line_item_adUnit.save() 
                            
            return HttpResponseRedirect(reverse('supply:inventory'))
        else:
            err_invalid_new_line_input = 'invalid new line input'  
            return render(request, 'supply/line_new.html', {'errors':err_invalid_new_line_input, 'inputLineName':name_entry, 'inputPlatform':platform_entry, 'type':type_entry, 'inventory':adUnit_name_entry})
    else:
        all_AdUnit_list = AdUnit.objects.all()

        return render(request, "supply/line_new.html", {'all_AdUnit_list':all_AdUnit_list})

@login_required
def line_edit(request, line_id):
    return render(request, "supply/line_edit.html", {})
    
@login_required
def inventory(request):
    all_sites = Site.objects.all()

    return render(request, "supply/inventory.html", {'site_collection': all_sites})

@login_required
def site_new(request):

    if request.method == 'POST':
        
        form = site_form(request.POST)
        if form.is_valid():
            cleaned_form = form.cleaned_data

            site_model = Site()
            
            site_model.name = cleaned_form['site_name']
            site_model.url = cleaned_form['site_URL']
            site_model.pub = Publisher.objects.get(pk=1)
            site_model.category = "hard_coded"
            
            site_model.save()
            
            return HttpResponseRedirect('/supply/inventory/')
            
        elif form.errors:
         
            return render(request, 'supply/site_new.html', {'form': form})    #form.errors accessed in view.py        
    else:
        return render(request, 'supply/site_new.html') 
        
@login_required
def site_edit(request, site_id):  
      
    site_to_edit = Site.objects.get(id=site_id)

    if request.method == 'POST':

        form = site_form(request.POST)
        
        if form.is_valid():
            cleaned_form = form.cleaned_data
   
            site_to_edit.name = cleaned_form['site_name']
            site_to_edit.url = cleaned_form['site_URL']

            site_to_edit.save()
            
            return HttpResponseRedirect('/supply/inventory/')
 
        else:
            err_invalid_new_order_input = 'Invalid site editing'  
            return render(request, 'supply/site_edit.html', {'errors':err_invalid_new_order_input, 'site_id':site_id, 'name':site_to_edit.name, 'url':site_to_edit.url})
    else:

        return render(request, 'supply/site_edit.html', {'site_id':site_id, 'name':site_to_edit.name, 'url':site_to_edit.url})       
    
@login_required
def adunits(request):
    return render(request, "supply/adunits.html", {})
        
@login_required
def adunit_new(request, site_id):
    return render(request, "supply/adunit_new.html", {})
    
@login_required
def adunit_edit(request, adunit_id):
    return render(request, "supply/adunit_edit.html", {})

@login_required
def reports(request):
    return render(request, "supply/reports.html", {})

@login_required
def reports_sites(request):
    return render(request, "supply/reports_sites.html", {})

@login_required
def report_detail(request, report_id):
    return render(request, "supply/report_detail.html", {})
