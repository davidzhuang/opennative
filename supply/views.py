from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms
from supply.models import *
from accounts.models import UserProfile
from supply.forms import site_form
from django.db import models

from datetime import date, datetime, time, timedelta

def get_user_publisher(user):
    try:
        return user.userprofile.pub
    except UserProfile.DoesNotExist:
        return None

@login_required
def index(request):
    pub = get_user_publisher(request.user)
    if pub == None:
        return HttpResponseRedirect(reverse('accounts:error', kwargs={'type':'account'}))

    all_orders = Order.objects.filter(pub=pub)
    return render(request, "supply/index.html", {'order_collection': all_orders})

@login_required
def order_new(request):
    user = request.user
    pub = get_user_publisher(user)
    if pub == None:
        return HttpResponseRedirect(reverse('accounts:error', kwargs={'type':'account'}))

    if request.method == 'POST':
        name_entry=request.POST.get('inputOrderName')
        company_entry=request.POST.get('inputCompany')

        if ( name_entry and company_entry):
            order = Order()
            order.name = name_entry
            order.company= company_entry
            order.status = 'DFT'
            order.creator = user.username
            order.pub = pub 
            
            order.save();             
            return HttpResponseRedirect(reverse('supply:index'))
        else:
            err_invalid_new_order_input = 'invalid new order input'  
            return render(request, reverse('supply/order_new.html', args=(order_id,)), {'errors':err_invalid_new_order_input, 'name':name_entry, 'company':company_entry})
    else:
        return render(request, 'supply/order_new.html', {})       

@login_required
def order_edit(request, order_id):
    user_pub = get_user_publisher(request.user)
    if user_pub == None:
        return HttpResponseRedirect(reverse('accounts:error', kwargs={'type':'account'}))
        
    order_to_edit = Order.objects.get(id=order_id)
    if user_pub != order_to_edit.pub:
        return HttpResponseRedirect(reverse('supply:error', kwargs={'type':'permission'}))

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
#   pub = get_user_publisher(request.user)
#  if pub == None:
#        return HttpResponseRedirect(reverse('accounts:error', kwargs={'type':'account'}))

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
    #field.choice lookup in template
    l= LineItem()

    errors = []
    adUnit_name_entry_list = AdUnit.objects.all()
    
    if request.method == 'POST':        
        input_queryDict = {}
        
        for key in request.POST.iterkeys():
            input_queryDict[key] = request.POST.getlist(key)
        
        name_entry = input_queryDict['inputLineName'][0]
        
        if not name_entry:
            errors.append('Name')
        
        platform_entry = input_queryDict['inputPlatform'][0]
        
        if not platform_entry:
            errors.append('Platform')
            
        type_entry = input_queryDict['type'][0]
        if not type_entry:
            errors.append('Type')
        
        #multiple choice, passed in as dictionary
        if 'inventory' in input_queryDict:
            adUnit_name_entry_list = input_queryDict['inventory']

        else:
            errors.append('Inventory')

        if len(errors)==0:

            new_line_item = LineItem()
            new_line_item.name = name_entry
            new_line_item.platform = platform_entry
            new_line_item.order= Order.objects.get(id = order_id)
            new_line_item.type = type_entry
            
            #non-mandatory attributes 
            new_line_item.status = 'DFT'
            
            #hardcoded date/time for testing purposes

            new_line_item.start_date = str(date.today())
            new_line_item.start_time = str(datetime.now().time()).split('.')[0]
            new_line_item.end_date = str(date.today() + timedelta(days=30)) #run add for a month
            new_line_item.end_time = str(datetime.now().time()).split('.')[0]

            new_line_item.dlv_priority = 1
             
            new_line_item.save() 
            
            for item in adUnit_name_entry_list: 
                new_line_item.adunits.add(item)
                                         
            return HttpResponseRedirect(reverse('supply:lines'))
        else:
            
            adUnit_selected_list =[]

            #mark previously selected items?            
            if (len(adUnit_name_entry_list) >0):
                adUnit_selected_list = adUnit_name_entry_list
                adUnit_name_entry_list = AdUnit.objects.all()
             
            return render(request, 'supply/line_new.html', {'order_id': order_id, 'errors':'Invalid input for '+ str(errors), 'inputLineName':name_entry, 'inputPlatform':platform_entry, 'type':type_entry, 'adUnit_name_entry_list':adUnit_name_entry_list, 'line_item':l})
    else:
        pub = get_user_publisher(request.user)
        if pub == None:
            return HttpResponseRedirect(reverse('accounts:error', kwargs={'type':'account'}))

        adUnit_name_entry_list = AdUnit.objects.all()
        return render(request, 'supply/line_new.html', {'order_id': order_id, 'adUnit_name_entry_list':adUnit_name_entry_list, 'line_item':l})

@login_required
def line_edit(request, line_id):

    #user_pub = get_user_publisher(request.user)
    #if user_pub == None:
    #   return HttpResponseRedirect(reverse('accounts:error', kwargs={'type':'account'}))
        
    line_to_edit = LineItem.objects.get(id=line_id)
    #if user_pub != order_to_edit.pub:
    #    return HttpResponseRedirect(reverse('supply:error', kwargs={'type':'permission'}))

    change_flags = []
    adUnit_name_entry_list = AdUnit.objects.all()
    
    if request.method == 'POST':        
        input_queryDict = {}
        
        for key in request.POST.iterkeys():
            input_queryDict[key] = request.POST.getlist(key)
        
        name_entry = input_queryDict['inputLineName'][0]
        if name_entry:
            change_flags.append('Name')
        
        platform_entry = input_queryDict['platform'][0]
        if not platform_entry:
            change_flags.append('Platform')
            
        type_entry = input_queryDict['type'][0]
        if not type_entry:
            change_flags.append('Type')
        
        #multiple choice, passed in as dictionary
        if 'inventory' in input_queryDict:
            adUnit_name_entry_list = input_queryDict['inventory']

        else:
            change_flags.append('Inventory')
            
        if len(change_flags)>0:
            if 'Name' in change_flags:
                line_to_edit.name = name_entry
            if 'Platform' in change_flags:
                line_to_edit.platform = platform_entry
            if 'Type' in change_flags:    
                line_to_edit.type = type_entry

			#need to also take care of adunit addition and removal here            
            line_to_edit.save() 
                                     
            return HttpResponseRedirect(reverse('supply:lines'))
        else:
            
            adUnit_selected_list =[]

            #mark previously selected items?            
            if (len(adUnit_name_entry_list) >0):
                adUnit_selected_list = adUnit_name_entry_list
                adUnit_name_entry_list = AdUnit.objects.all()
             
            return render(request, 'supply/line_edit.html', {'line_id': line_id, 'change_flags':'Changed these fileds: '+ str(change_flags), 'inputLineName':name_entry, 'inputPlatform':platform_entry, 'type':type_entry, 'adUnit_name_entry_list':adUnit_name_entry_list, 'line_item':l})
    else:
        pub = get_user_publisher(request.user)
        if pub == None:
            return HttpResponseRedirect(reverse('accounts:error', kwargs={'type':'account'}))

        adUnit_name_entry_list = AdUnit.objects.all()
        return render(request, 'supply/line_edit.html', {'line_id': line_id, 'adUnit_name_entry_list':adUnit_name_entry_list, 'line_item':line_to_edit})







                        
           # order_to_edit.save();             
            #return HttpResponseRedirect(reverse('supply:index'))
        #else:
         #   err_invalid_new_order_input = 'Invalid order editing'  
          #  return render(request, 'supply/order_edit.html', {'change_flags':err_invalid_new_order_input, 'name':name_entry, 'company':company_entry})
    #else:
     #   return render(request, 'supply/order_edit.html', {'id':order_id, 'name':order_to_edit.name, 'company':order_to_edit.company})       
    



 #   return render(request, "supply/line_edit.html", {})
    
@login_required
def inventory(request):
    pub = get_user_publisher(request.user)
    if pub == None:
        return HttpResponseRedirect(reverse('accounts:error', kwargs={'type':'account'}))
        
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
    pub = get_user_publisher(request.user)
    if pub == None:
        return HttpResponseRedirect(reverse('accounts:error', kwargs={'type':'account'}))
        
    return render(request, "supply/adunits.html", {})
        
@login_required
def adunit_new(request, site_id):
    return render(request, "supply/adunit_new.html", {})
    
@login_required
def adunit_edit(request, adunit_id):
    return render(request, "supply/adunit_edit.html", {})

@login_required
def reports(request):
    pub = get_user_publisher(request.user)
    if pub == None:
        return HttpResponseRedirect(reverse('accounts:error', kwargs={'type':'account'}))
        
    return render(request, "supply/reports.html", {})

@login_required
def reports_sites(request):
    return render(request, "supply/reports_sites.html", {})

@login_required
def report_detail(request, report_id):
    return render(request, "supply/report_detail.html", {})

def error(request, type):
    errors = { "permission" : { "title":"Permission Error",
                             "msg":"Your are not authorized to access this information. Please check your request." },
             }
    try:
        error = errors[type]
    except KeyError:
        error = { "title":"Operation Error",
                  "msg":"Error in your operation." }
    return render(request, "supply/error.html", {"error" : error })

