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
        
    class adUnit_by_site:
        site_with_adUnit = None
        entire_adUnit_list = []
      
    new_line_item= LineItem()
      
    errors = []
    adUnit_selected_list =[] #retrieved from POST
    
    adUnit_by_site_list = []  #generated for both GET and POST from database
        
    #field.choice lookup in template
    new_line_item= LineItem()
            
    current_site_list = Site.objects.filter(pub=pub)
    all_orders = Order.objects.filter(pub=pub)
    
    for item in current_site_list:
        element = adUnit_by_site()        
        if (len(AdUnit.objects.filter(site=item)) > 0):
            element.site_with_adUnit = item
            element.entire_adUnit_list = AdUnit.objects.filter(site=item)
            adUnit_by_site_list.append(element)
 
    if request.method == 'POST':   
        order_name_entry=request.POST.get('inputOrderName')
        order_company_entry=request.POST.get('inputCompany')
        line_name_entry = request.POST['inputLineName'] 
        line_platform_entry = request.POST['inputPlatform']
        line_type_entry = request.POST['type']
        
        if not order_name_entry:
            errors.append('inputOrderName')
        if not order_company_entry:
            errors.append('inputCompany') 
        if not line_name_entry:
            errors.append('Line Item Name')
        if not line_platform_entry:
            errors.append('Line Item Platform')        
        if not line_type_entry:
            errors.append('Line Item Type')
        
        inventory_queryDict = []
        
        inventory_queryDict = request.POST.getlist('inventory')
        if (len(inventory_queryDict) > 0 ):
            for id in inventory_queryDict:#received adunit.id from POST, convert to object
                adUnit_selected_list.append(AdUnit.objects.get(pk=id)) 
        else:
            errors.append('Inventory')
                     
        # create order 
        if ( len(errors) == 0 ):
                    
            order = Order()
            order.pub = pub 
            order.name = order_name_entry
            order.company= order_company_entry
            order.status = 'DFT'
            order.creator = user.username
             
        #create new line                                
            new_line_item.name = line_name_entry
            new_line_item.platform = line_platform_entry
            new_line_item.type = line_type_entry
            
            #non-mandatory attributes 
            new_line_item.status = 'DFT'            
            #hardcoded date/time for testing purposes
            new_line_item.start_date = str(date.today())
            new_line_item.start_time = str(datetime.now().time()).split('.')[0]
            new_line_item.end_date = str(date.today() + timedelta(days=30)) #run add for a month
            new_line_item.end_time = str(datetime.now().time()).split('.')[0]
            new_line_item.dlv_priority = 1

#database access
            order.save()  
                           
            if not order:            
                errors = 'failure saving new order'  
                return render(request, reverse('supply/order_new.html'), {'errors':str(errors), 'inputOrderName':order_name_entry, 'inputCompany':order_company_entry, 'inputLineName':line_name_entry, 'inputPlatform':line_platform_entry, 'type':line_type_entry, 'adUnit_by_site_list':adUnit_by_site_list, 'adUnit_selected_list':adUnit_selected_list,'line_item':new_line_item})

            new_line_item.order= order
                
            new_line_item.save() 

            if not new_line_item:
                errors = 'failure saving new line for order' 
                return render(request, 'supply/order_new.html', {'errors':str(errors), 'inputOrderName':order_name_entry, 'inputCompany':order_company_entry, 'inputLineName':line_name_entry, 'inputPlatform':line_platform_entry, 'type':line_type_entry, 'adUnit_by_site_list':adUnit_by_site_list, 'adUnit_selected_list':adUnit_selected_list, 'line_item':new_line_item})                                         

            for item in adUnit_selected_list: 
                new_line_item.adunits.add(item)
                                
            return HttpResponseRedirect(reverse('supply:index'))

        else: #invalid input
            return render(request, 'supply/order_new.html', { 'errors':str(errors), 'inputOrderName':order_name_entry, 'inputCompany':order_company_entry, 'inputLineName':line_name_entry, 'inputPlatform':line_platform_entry, 'type':line_type_entry, 'adUnit_by_site_list':adUnit_by_site_list, 'adUnit_selected_list':adUnit_selected_list,'line_item':new_line_item})

    else: # get request
        return render(request, 'supply/order_new.html', {'adUnit_by_site_list':adUnit_by_site_list,'line_item':new_line_item})       

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
    pub = get_user_publisher(request.user)
    if pub == None:
        return HttpResponseRedirect(reverse('accounts:error', kwargs={'type':'account'}))
        
    all_orders_with_line_items = []
    all_line_items =[]
    
    class all_lines_by_order:
        line_item_list = []
        order = None
        
    all_order_items = Order.objects.filter(pub=pub)
    for item in all_order_items:
        all_line_items +=  LineItem.objects.filter(order=item)
    
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
    pub = get_user_publisher(request.user)
    if pub == None:
        return HttpResponseRedirect(reverse('accounts:error', kwargs={'type':'account'}))

    current_order = Order.objects.get(id=order_id)

    if pub != current_order.pub:
        return HttpResponseRedirect(reverse('supply:error', kwargs={'type':'permission'}))

    errors = []
    adUnit_selected_list =[] #retrieved from POST
    
    adUnit_by_site_list = []  #generated for both GET and POST from database

    class adUnit_by_site:
        site_with_adUnit = None
        entire_adUnit_list = []
        
    #field.choice lookup in template
    new_line_item= LineItem()
    
    current_site_list = Site.objects.filter(pub=pub)
    
    for item in current_site_list:    
        element = adUnit_by_site()
        if (len(AdUnit.objects.filter(site=item)) > 0):#only add those sites with adUnits for display
            element.site_with_adUnit = item
            element.entire_adUnit_list = AdUnit.objects.filter(site=item)
            adUnit_by_site_list.append(element)      
   
    if request.method == 'POST':   
        
        name_entry = request.POST['inputLineName'] 
        platform_entry = request.POST['inputPlatform']
        type_entry = request.POST['type']
        
        if not name_entry:
            errors.append('Name')
        if not platform_entry:
            errors.append('Platform')        
        if not type_entry:
            errors.append('Type')
        
        inventory_queryDict = []

        inventory_queryDict = request.POST.getlist('inventory')
        if (len(inventory_queryDict) > 0 ):
            for id in inventory_queryDict:#received adunit.id from POST, convert to object
                adUnit_selected_list.append(AdUnit.objects.get(pk=id)) 
        else:
            errors.append('Inventory')

        if len(errors)==0:
            new_line_item.name = name_entry
            new_line_item.platform = platform_entry
            new_line_item.order= current_order
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

            for item in adUnit_selected_list: 
                new_line_item.adunits.add(item)
           
            return HttpResponseRedirect(reverse('supply:lines'))
        else:
            return render(request, 'supply/line_new.html', {'errors':str(errors), 'order_id': order_id, 'inputLineName':name_entry, 'inputPlatform':platform_entry, 'type':type_entry, 'adUnit_by_site_list':adUnit_by_site_list, 'adUnit_selected_list':adUnit_selected_list,'line_item':new_line_item})
    else:
        return render(request, 'supply/line_new.html', {'order_id': order_id, 'adUnit_by_site_list':adUnit_by_site_list, 'line_item':new_line_item})

@login_required
def line_edit(request, line_id):
    user_pub = get_user_publisher(request.user)
    if user_pub == None:
        return HttpResponseRedirect(reverse('accounts:error', kwargs={'type':'account'}))

    line_to_edit = LineItem.objects.get(id=line_id)

    if user_pub != line_to_edit.order.pub:
        return HttpResponseRedirect(reverse('supply:error', kwargs={'type':'permission'}))

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
             
            return render(request, 'supply/line_edit.html', {'line_id': line_id, 'change_flags':'Changed these fileds: '+ str(change_flags), 'inputLineName':name_entry, 'inputPlatform':platform_entry, 'type':type_entry, 'adUnit_name_entry_list':adUnit_name_entry_list, 'line_item':line_to_edit})
    else:
        pub = get_user_publisher(request.user)
        if pub == None:
            return HttpResponseRedirect(reverse('accounts:error', kwargs={'type':'account'}))

        adUnit_name_entry_list = AdUnit.objects.all()
        return render(request, 'supply/line_edit.html', {'line_id': line_id, 'adUnit_name_entry_list':adUnit_name_entry_list, 'line_item':line_to_edit})
    
@login_required
def inventory(request):
    pub = get_user_publisher(request.user)
    if pub == None:
        return HttpResponseRedirect(reverse('accounts:error', kwargs={'type':'account'}))
        
    all_sites = Site.objects.filter(pub=pub)
    return render(request, "supply/inventory.html", {'site_collection': all_sites})

@login_required
def site_new(request):
    pub = get_user_publisher(request.user)
    if pub == None:
        return HttpResponseRedirect(reverse('accounts:error', kwargs={'type':'account'}))

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
    user_pub = get_user_publisher(request.user)
    if user_pub == None:
        return HttpResponseRedirect(reverse('accounts:error', kwargs={'type':'account'}))
      
    site_to_edit = Site.objects.get(id=site_id)

    if user_pub != site_to_edit.pub:
        return HttpResponseRedirect(reverse('supply:error', kwargs={'type':'permission'}))

    pub = get_user_publisher(request.user)
    if pub == None:
        return HttpResponseRedirect(reverse('accounts:error', kwargs={'type':'account'}))

    current_order = Order.objects.get(id=order_id)

    if pub != current_order.pub:
        return HttpResponseRedirect(reverse('supply:error', kwargs={'type':'permission'}))


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
            new_line_item.order= current_order
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
        return render(request, 'supply/line_new.html', {'order_id': order_id, 'adUnit_name_entry_list':adUnit_name_entry_list, 'adUnit_item':l})

@login_required
def adunits(request):
    pub = get_user_publisher(request.user)
    if pub == None:
        return HttpResponseRedirect(reverse('accounts:error', kwargs={'type':'account'}))
     
    all_adunits_for_user = []
    all_sites_for_user = Site.objects.filter(pub=pub)
    for site in all_sites_for_user:
        all_adunits_for_user += AdUnit.objects.filter(site=site)
 
    return render(request, "supply/adunits.html", {'all_sites': all_sites_for_user, 'all_adunits': all_adunits_for_user})
        
@login_required
def adunit_new(request, site_id):
    pub = get_user_publisher(request.user)
    if pub == None:
        return HttpResponseRedirect(reverse('accounts:error', kwargs={'type':'account'}))

    current_site = Site.objects.get(id=site_id)

    if pub != current_site.pub:
        return HttpResponseRedirect(reverse('supply:error', kwargs={'type':'permission'}))

    errors = []
    ad_unit= AdUnit()
    
    if request.method == 'POST':        
        input_queryDict = {}
        
        for key in request.POST.iterkeys():
            input_queryDict[key] = request.POST.getlist(key)
        
        name_entry = input_queryDict['name'][0]
        
        if not name_entry:
            errors.append('Name')
        
        type_entry = input_queryDict['type'][0]
        
        if not type_entry:
            errors.append('Type')
            
        target_entry = input_queryDict['target'][0]
        if not target_entry:
            errors.append('Target')
        
        size_entry = input_queryDict['size'][0]
        
        if not size_entry:
            errors.append('Size')
            
        desc_entry = input_queryDict['desc'][0]
        if not desc_entry:
            errors.append('Description')
            
        if len(errors)==0:
            ad_unit.name = name_entry
            ad_unit.targetwindow = target_entry
            ad_unit.sizes= size_entry
            ad_unit.site= current_site
            ad_unit.type = type_entry
            ad_unit.desc = desc_entry
            ad_unit.save() 
                  
            return HttpResponseRedirect(reverse('supply:adunits'))
        else:
             
            return render(request, 'supply/adunit_new.html', {'site_id': site_id, 'errors':'Invalid input for '+ str(errors), 'name':name_entry, 'target':target_entry, 'type':type_entry, 'size':size_entry, 'desc':desc_entry, 'ad_unit':ad_unit})
    else:
        pub = get_user_publisher(request.user)
        if pub == None:
            return HttpResponseRedirect(reverse('accounts:error', kwargs={'type':'account'}))

        adUnit_name_entry_list = AdUnit.objects.all()
        return render(request, 'supply/adunit_new.html', {'site_id': site_id, 'ad_unit':ad_unit})
    
@login_required
def adunit_edit(request, adunit_id):
    user_pub = get_user_publisher(request.user)
    if user_pub == None:
        return HttpResponseRedirect(reverse('accounts:error', kwargs={'type':'account'}))

    adUnit_to_edit = AdUnit.objects.get(id=adunit_id)

    if user_pub != adUnit_to_edit.site.pub:
        return HttpResponseRedirect(reverse('supply:error', kwargs={'type':'permission'}))

    change_flags = []

    if request.method == 'POST':        
        input_queryDict = {}
        
        for key in request.POST.iterkeys():
            input_queryDict[key] = request.POST.getlist(key)
        
        name_entry = input_queryDict['name'][0]
        if name_entry:
            change_flags.append('Name')
        
        target_entry = input_queryDict['target'][0]
        if target_entry:
            change_flags.append('Target')
            
        type_entry = input_queryDict['type'][0]
        if type_entry:
            change_flags.append('Type')

        size_entry = input_queryDict['size'][0]
        if size_entry:
            change_flags.append('Size')
            
        desc_entry = input_queryDict['desc'][0]
        if type_entry:
            change_flags.append('Description')
       
        if len(change_flags)>0:
            if 'Name' in change_flags:
                adUnit_to_edit.name = name_entry
            if 'Target' in change_flags:
                adUnit_to_edit.targetwindow = target_entry
            if 'Type' in change_flags:    
                adUnit_to_edit.type = type_entry
            if 'Size' in change_flags:
                adUnit_to_edit.sizes = size_entry
            if 'Description' in change_flags:    
                adUnit_to_edit.desc = desc_entry
                          
            adUnit_to_edit.save() 
                         
            return HttpResponseRedirect(reverse('supply:adunits'))
        else:

            return render(request, 'supply/adunit_edit.html', {'adunit_id': adunit_id, 'change_flags':'Tried to change these fileds, but failed: '+ str(change_flags), 'name':name_entry, 'target':target_entry, 'type':type_entry, 'size':size_entry, 'desc':desc_entry, 'ad_unit':adUnit_to_edit})
    else:
        return render(request, 'supply/adunit_edit.html', {'adunit_id': adunit_id, 'ad_unit':adUnit_to_edit})

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

