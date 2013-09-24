from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
from supply.models import Publisher
from accounts.models import UserProfile
import re

class FormErrors:
    pass

def signin(request):
    logout(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('supply:index'))
            else:
                # Return a 'disabled account' error message
                return render(request, "accounts/signin.html", {'error': 'Disabled account, please re-activate the account, or use a different account'})
        else:
            # Return an 'invalid login' error message.
            return render(request, "accounts/signin.html", {'error': 'Username/email and password do not match'})
    else:
        return render(request, "accounts/signin.html", {})

def signup(request):
    if request.method == 'POST':
        # first, get all required fields
        username = strip_tags(request.POST['username'].strip())
        email = strip_tags(request.POST['email'].strip())
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        lastname = strip_tags(request.POST['lastname'].strip())
        companyname = strip_tags(request.POST['companyname'].strip())
        phone = strip_tags(request.POST['phone'].strip())

        # validate all required fields
        errors = FormErrors()
        has_error = False

        if not username:
            errors.username = "This is a required field"
            has_error = True

        if not email:
            errors.email = "This is a required field"
            has_error = True

        if not password:
            errors.password = "This is a required field"
            has_error = True
        elif len(password) < 8:
            errors.password = "Password too short"
            has_error = True
        elif re.search(r'\d', password) == None:
            errors.password = "Password must contain at least 1 number"
            has_error = True
        elif re.search(r'[A-Z]', password) == None:
            errors.password = "Password must contain at least 1 upper case letter"
            has_error = True
        elif re.search(r'[a-z]', password) == None:
            errors.password = "Password must contain at least 1 lower case letter"
            has_error = True

        if not password_confirm:
            errors.password_confirm = "This is a required field"
            has_error = True
        elif password_confirm != password:
            errors.password_confirm = "Passwords do not match"
            has_error = True

        if not lastname:
            errors.lastname = "This is a required field"
            has_error = True

        if not companyname:
            errors.companyname = "This is a required field"
            has_error = True

        if not phone:
            errors.phone = "This is a required field"
            has_error = True

        if has_error:
            return render(request, "accounts/signup.html", {'errors' : errors, })

        # save user info
        user = User.objects.create_user(username, email, password)
        user.first_name = request.POST['firstname']
        user.last_name = lastname
        user.save()

        pub = Publisher()
        pub.name = companyname
        pub.phone = phone
        pub.address = strip_tags(request.POST['address'])
        pub.address2 = strip_tags(request.POST['address2'])
        pub.city = strip_tags(request.POST['city'])
        pub.state = strip_tags(request.POST['state'])
        pub.province = strip_tags(request.POST['province'])
        pub.zipcode = strip_tags(request.POST['zipcode'])
        pub.country = strip_tags(request.POST['country'])
        pub.save()

        profile = UserProfile()
        profile.user = user;
        profile.pub = pub;
        profile.save()

        login(request, user)
        return HttpResponseRedirect(reverse('supply:inventory'))

    else:
        return render(request, "accounts/signup.html", {})

def error(request, type):
    errors = { "account" : { "title":"Account Error", 
                             "msg":"Your account has no publisher information, please set up your publisher account before proceeding" },
             }
    try:
        error = errors[type]
    except KeyError:
        error = { "title":"Account Error",
                  "msg":"Error in your account." }
    return render(request, "accounts/error.html", {"error" : error })

