from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import * 
from django.utils.html import strip_tags
from django.db import IntegrityError
from django import forms
from supply.models import Publisher
from accounts.models import UserProfile
from django.contrib.auth.views import password_reset, password_reset_confirm

class FormErrors:
    pass

class SignupForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.CharField(max_length=75)
    password = forms.CharField(max_length=60)
    password_confirm = forms.CharField(max_length=60)
    firstname = forms.CharField(max_length=30, required=False)
    lastname = forms.CharField(max_length=30)
    companyname = forms.CharField(max_length=64)
    phone = forms.CharField(max_length=32)
    address = forms.CharField(max_length=64, required=False)
    address2 = forms.CharField(max_length=64, required=False)
    city = forms.CharField(max_length=32, required=False)
    state = forms.CharField(max_length=32, required=False)
    zipcode = forms.CharField(max_length=32, required=False)
    province = forms.CharField(max_length=64, required=False)
    country = forms.CharField(max_length=64, required=False)

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

def signedout(request):
    logout(request)
    msg = 'You have successfully signed out.'
    return render(request, "accounts/signedout.html", {'msg':msg})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        # form will validate basic rules
        if not form.is_valid():
            return render(request, "accounts/signup.html", {'form' : form, })

        # we also need to validate advanced rules here
        errors = FormErrors()
        has_error = False

        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        password_confirm = form.cleaned_data['password_confirm']

        if len(password) < 8:
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

        if password_confirm != password:
            errors.password_confirm = "Passwords do not match"
            has_error = True

        if has_error:
            return render(request, "accounts/signup.html", {'form' : form, 'errors' : errors, })

        # save user info
        try:
            user = User.objects.create_user(username, email, password)
        except IntegrityError:
            errors.username = "This username is already in use, please pick a different username"
            return render(request, "accounts/signup.html", {'form' : form, 'errors' : errors, })

        user.first_name = request.POST['firstname']
        user.last_name = form.cleaned_data['lastname']
        try:
            user.save()
        except IntegrityError:
            errors.username = "This username is already in use, please pick a different username"
            return render(request, "accounts/signup.html", {'form' : form, 'errors' : errors, })

        pub = Publisher()
        pub.name = form.cleaned_data['companyname']
        pub.phone = form.cleaned_data['phone']
        pub.address = form.cleaned_data['address']
        pub.address2 = form.cleaned_data['address2']
        pub.city = form.cleaned_data['city']
        pub.state = form.cleaned_data['state']
        pub.province = form.cleaned_data['province']
        pub.zipcode = form.cleaned_data['zipcode']
        pub.country = form.cleaned_data['country']
        try:
            pub.save()
        except IntegrityError:
            errors.companyname = "This company name is already in use, please use a different company name, or contact us to claim your company name"
            return render(request, "accounts/signup.html", {'form' : form, 'errors' : errors, })

        profile = UserProfile()
        profile.user = user;
        profile.pub = pub;
        profile.save()

        # tell user he's signed up and ask him to sign in
        return HttpResponseRedirect(reverse('accounts:signup_done'))
    else:
        return render(request, "accounts/signup.html", {})

def signup_done(request):
    return render(request, "accounts/signup_done.html", {})

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

#not tested due to email server
def reset_confirm(request, uidb36=None, token=None):
    return password_reset_confirm(request, template_name='accounts/reset_confirm.html',
        uidb36=uidb36, token=token, post_reset_redirect=reverse('accounts:signin'))

#not tested due to email server
def reset(request):
    return password_reset(request, template_name='accounts/reset_form.html',
        email_template_name='accounts/reset_email.html',
        subject_template_name='accounts/reset_subject.txt',
        post_reset_redirect=reverse('accounts:signin'))

