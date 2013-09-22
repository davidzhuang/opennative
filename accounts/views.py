from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
                return render(request, "accounts/signin.html", {'errors': 'Disabled account, please re-activate, or use a different account'})
        else:
            # Return an 'invalid login' error message.
            return render(request, "accounts/signin.html", {'errors': 'Username/email and password do not match'})
    else:
        return render(request, "accounts/signin.html", {})

def error(request, type):
    errors = { "account" : { "title":"Account Error", 
                             "msg":"Your account has no publisher information, please set up your publisher account before proceeding" },
             }
    error = errors[type]
    return render(request, "accounts/error.html", {"error" : error })

