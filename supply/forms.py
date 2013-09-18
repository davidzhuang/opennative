from django import forms
from supply.models import *

class site_form(forms.Form):
    site_name = forms.CharField(max_length=64)
    site_URL = forms.CharField(max_length=64)

 
