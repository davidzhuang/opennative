from django.db import models
from django.contrib.auth.models import User
from supply.models import Publisher

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=32, blank=True)
    title = models.CharField(max_length=32, blank=True)
    pub = models.ForeignKey(Publisher, blank=True, null=True)
    def __unicode__(self):
        return self.user.username
