from django.core.management.base import BaseCommand, CommandError
from supply.models import Publisher, Site, AdUnit
from supply.activation.supplyutil import SupplyUtil
import redis

class Command(BaseCommand):
    args = ''
    help = 'Push full supply data to ad server'

    def handle(self, *args, **options):
        #self.stdout.write("args: ")
        #for arg in args:
        #    self.stdout.write('%s' %arg)

        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        
        units = AdUnit.objects.all()
        for unit in units:
            SupplyUtil.pushUnit(r, unit)

            #key = ''.join(['unit:', unit.name])
            #value = ''.join(['{"site":"', str(unit.site.id), '","type":"', unit.type, '","target":"', unit.targetwindow, '"}'])
            ##print "pub: ", unit.site.pub
            #self.stdout.write('key: %s, value: %s' %(key, value))
            #r.zadd(key, 0, value)
            

