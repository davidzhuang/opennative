from django.contrib import admin

from supply.models import Publisher, User, Site, AdUnit
from supply.models import Order, LineItem, Creative
from supply.models import LineItemAdUnit, CustomTarget, GeoTarget

admin.site.register(Publisher)
admin.site.register(User)
admin.site.register(Site)
admin.site.register(AdUnit)
admin.site.register(Order)

class AdUnitInline(admin.StackedInline):
    model = LineItemAdUnit
    extra = 1

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
    ]
    inlines = [AdUnitInline, CustomTargetInline, GeoTargetInline, CreativeInline]
    list_display = ('name', 'platform', 'type')

admin.site.register(LineItem, LineItemAdmin)
