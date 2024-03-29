from django.contrib import admin

from supply.models import Publisher, Site, AdUnit
from supply.models import Order, LineItem, Creative
from supply.models import CustomTarget, GeoTarget

from accounts.models import UserProfile

admin.site.register(Publisher)
admin.site.register(UserProfile)
admin.site.register(Site)
admin.site.register(AdUnit)
admin.site.register(Order)

class CustomTargetInline(admin.StackedInline):
    model = CustomTarget
    extra = 1

class GeoTargetInline(admin.StackedInline):
    model = GeoTarget
    extra = 1

class CreativeInline(admin.StackedInline):
    model = Creative
    extra = 1

class LineItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['name', 'order', 'platform', 'status']}),
        ('Schedule', {'fields':['start_date', 'start_time', 'end_date', 'end_time']}),
        ('Settings', {'fields':['type', 'priority', 'percentage', 'price', 'quantity', 'goal', 'budget']}),
        ('Delivery', {'fields':['deliver', 'dlv_priority']}),
        ('AdUnits', {'fields':['adunits']}),
    ]
    inlines = [CustomTargetInline, GeoTargetInline, CreativeInline]
    list_display = ('name', 'platform', 'type')

admin.site.register(LineItem, LineItemAdmin)
