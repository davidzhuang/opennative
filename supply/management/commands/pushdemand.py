from django.core.management.base import BaseCommand, CommandError
from supply.models import Order, LineItem, AdUnit
from supply.models import Creative, CustomTarget, GeoTarget
from supply.models import LineItemAdUnit
from supply.activation.demandutil import DemandUtil
import redis

class Command(BaseCommand):
    args = ''
    help = 'Push full demand data to ad server'

    def handle(self, *args, **options):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)

        # push LineItems and related creatives
        lines = LineItem.objects.all()
        for ln in lines:
            DemandUtil.pushLine(r, ln)

        # push LineItemAdUnit reverse index
        units = AdUnit.objects.all()
        for u in units:
            DemandUtil.pushUnitToLineIndex(r, u)

"""
            key = ''.join(['line:', str(ln.id)])

            # do 2 things for each creative:
            #    1. push creative
            #    2. add creative id to crtv_str for line
            #
            creatives = Creative.objects.filter(line=ln.id)
            crtv_str = '['
            first = True
            for creative in creatives:
                crtv_key = 'crtv:' + str(creative.id)
                crtv_value = creative.crtv
                self.stdout.write('crtv_key: %s, crtv_value: %s' %(crtv_key, crtv_value))
                r.set(crtv_key, crtv_value)
                if (first == True):
                    crtv_str += '"' + str(creative.id) + '"'
                    first = False
                else:
                    crtv_str += ',"' + str(creative.id) + '"'
                    first = False
            crtv_str += ']'

            value = ''.join(['{"crtv":', crtv_str, ',"deliver":"', ln.deliver, '"}'])
            self.stdout.write('key: %s, value: %s' %(key, value))
            r.set(key, value)
"""

"""
            key = ''.join(['unit:', u.name])
            unitlines = LineItemAdUnit.objects.filter(unit=u.id)
            for unitline in unitlines:
                line = LineItem.objects.get(id=unitline.line.id)
                score = line.dlv_priority
                value = str(line.id)
                self.stdout.write('key: %s, score: %d, value: %s' %(key, score, value))
                r.zadd(key, score, value)
"""

