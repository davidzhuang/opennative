import sys
from supply.models import LineItem
from supply.models import Creative, CustomTarget, GeoTarget

# classes used: AdUnit
#               redis.StrictRedis

class DemandUtil:

    # pushLine(r, ln): push a LineItem to Redis
    # arguments: r : redis.StrictRedis
    #            ln : LineItem
    @staticmethod
    def pushLine(r, ln):
            key = ''.join(['line:', str(ln.id)])

            # do 2 things for each creative:
            #    1. push creative
            #    2. add creative id to crtv_str for line
            creatives = Creative.objects.filter(line=ln.id)
            crtv_str = '['
            first = True
            for creative in creatives:
                # push crtv
                crtv_key = 'crtv:' + str(creative.id)
                crtv_value = creative.crtv
                sys.stdout.write('crtv_key: %s, crtv_value: %s\n' %(crtv_key, crtv_value))
                r.set(crtv_key, crtv_value)
                # construct crtv_str
                if (first == True):
                    crtv_str += '"' + str(creative.id) + '"'
                    first = False
                else:
                    crtv_str += ',"' + str(creative.id) + '"'
                    first = False
            crtv_str += ']'
            value = ''.join(['{"crtv":', crtv_str, ',"deliver":"', ln.deliver, '"}'])
            sys.stdout.write('set: key: %s, value: %s\n' %(key, value))
            r.set(key, value)


    # pushUnitToLineIndex(r, u): push AdUnit-LineItem index to Redis
    # arguments: r : redis.StrictRedis
    #            u : AdUnit
    @staticmethod
    def pushUnitToLineIndex(r, u):
        key = ''.join(['unit:', str(u.id)])
        #unitlines = LineItemAdUnit.objects.filter(unit=u.id)
        unitlines = u.lineitem_set.all()
        for line in unitlines:
            #line = LineItem.objects.get(id=unitline.id)
            score = line.dlv_priority
            value = str(line.id)
            sys.stdout.write('zadd: key: %s, score: %d, value: %s\n' %(key, score, value))
            r.zadd(key, score, value)

