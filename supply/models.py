from django.db import models
from django.db.models.signals import post_save

class Publisher(models.Model):
    name = models.CharField(max_length=64, unique=True)
    url = models.CharField(max_length=64, blank=True)
    address = models.CharField(max_length=64)
    address2 = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=32)
    state = models.CharField(max_length=32, blank=True)
    zipcode = models.CharField(max_length=32, blank=True)
    province = models.CharField(max_length=64, blank=True)
    country = models.CharField(max_length=64)
    phone = models.CharField(max_length=32)
    phone2 = models.CharField(max_length=32, blank=True)
    def __unicode__(self):
        return self.name

class Site(models.Model):
    name = models.CharField(max_length=64, unique=True)
    pub = models.ForeignKey(Publisher)
    url = models.CharField(max_length=64, unique=True)
    category = models.CharField(max_length=16)
    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'pub')

class AdUnit(models.Model):
    AD_TYPES = (
        ('STD', 'Standard Display'),
        ('ISP', 'Native - In-Stream Short Post'),
        ('IIMG', 'Native - In-Stream Image'),
        ('IVID', 'Native - In-Stream Video'),
        ('LP', 'Native - Long Post'),
    )
    TARGET_WINDOW = (
        ('_top', '_top: Same Window'),
        ('_blank', '_blank: New Window'),
    )
    name = models.CharField(max_length=16)
    desc = models.CharField(max_length=128, blank=True)
    site = models.ForeignKey(Site)
    type = models.CharField(max_length=4, choices=AD_TYPES)
    sizes = models.CharField(max_length=32, blank=True)
    targetwindow = models.CharField(max_length=6, choices=TARGET_WINDOW, default='_top')
    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'site')


#class AdPlacement(models.Model):
#    name = models.CharField(max_length=16)
#    site = models.ForeignKey(Site)
#    units = models.ManyToManyField(AdUnit)
#
#    class Meta:
#        unique_together = ('name', 'site')


class Order(models.Model):
    ORDER_STATUS = (
        ('RDY', 'Ready'),
        ('DLV', 'Delivering'),
        ('PSD', 'Paused'),
        ('PND', 'Pending Approval'),
        ('DFT', 'Draft'),
        ('ACV', 'Archived'),
    )
    name = models.CharField(max_length=64)
    pub = models.ForeignKey(Publisher)
    creator = models.CharField(max_length=32)
    company = models.CharField(max_length=64)
    status = models.CharField(max_length=3, choices=ORDER_STATUS, default='DFT')
    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'pub')

class LineItem(models.Model):
    WEB = 'W'
    MOBILE = 'M'
    PLATFORM_TYPES = (
        (WEB, 'Web'),
        (MOBILE, 'Mobile'),
    )
    LINE_ITEM_TYPES = (
        ('XCL', 'Exclusive'),
        ('STD', 'Standard'),
        ('NTW', 'Network'),
        ('BLK', 'Bulk'),
        ('PRC', 'Price Priority'),
        ('HSE', 'House'),
    )
    LINE_ITEM_STATUS = (
        ('DLV', 'Delivering'),
        ('RDY', 'Ready'),
        ('PSD', 'Paused'),
        ('PND', 'Pending Approval'),
        ('CPL', 'Completed'),
        ('DFT', 'Draft'),
        ('ACV', 'Archived'),
        ('CRV', 'Missing Creatives'),
    )
    PRIORITY_VALUES = (
        ('H', 'High'),
        ('N', 'Normal'),
        ('L', 'Low'),
    )
    EVENLY = 'E'
    ASA = 'A'
    DELIVER_MODES = (
        (EVENLY, 'Evenly'),
        (ASA, 'As Soon As'),
    )
    name = models.CharField(max_length=64)
    order = models.ForeignKey(Order)
    platform = models.CharField(max_length=1, choices=PLATFORM_TYPES, default=WEB)
    status = models.CharField(max_length=3, choices=LINE_ITEM_STATUS, default='DFT')
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    type = models.CharField(max_length=3, choices=LINE_ITEM_TYPES)
    priority = models.CharField(max_length=1, choices=PRIORITY_VALUES, blank=True)
    percentage = models.DecimalField(max_digits=4, decimal_places=1, blank=True, default=100.0)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, default=1.00)
    quantity = models.PositiveIntegerField(blank=True, default=0)
    goal = models.PositiveIntegerField(blank=True, default=0)
    budget = models.FloatField(blank=True, default=0)
    deliver = models.CharField(max_length=1, choices=DELIVER_MODES, default=EVENLY)
    dlv_priority = models.PositiveSmallIntegerField()
    adunits = models.ManyToManyField(AdUnit)
    def __unicode__(self):
        return self.name

class CustomTarget(models.Model):
    line = models.ForeignKey(LineItem)
    kv = models.CharField(max_length=512)

class GeoTarget(models.Model):
    line = models.ForeignKey(LineItem)
    level = models.CharField(max_length=8)
    value = models.CharField(max_length=256)


class Creative(models.Model):
    name = models.CharField(max_length=64)
    line = models.ForeignKey(LineItem)
    type = models.CharField(max_length=4, choices=AdUnit.AD_TYPES)
    crtv = models.CharField(max_length=1024)
    def __unicode__(self):
        return self.name




# define and register for signals
def adunit_postsave(sender, **kwargs):
    print("got adunit save signal")
    keys = kwargs.keys()
    for key in keys:
        print key, ":", kwargs[key]

post_save.connect(adunit_postsave, sender=AdUnit, weak=False, dispatch_uid="adunit_1")

def lineitem_postsave(sender, **kwargs):
    print("got lineitem save signal")
    keys = kwargs.keys()
    for key in keys:
        print key, ":", kwargs[key]

post_save.connect(lineitem_postsave, sender=LineItem, weak=False, dispatch_uid="lineitem_1")


