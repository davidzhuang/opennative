# classes used: AdUnit
#               redis.StrictRedis

class SupplyUtil:

    @staticmethod
    def pushUnit(r, unit):
        # arguments: r : redis.StrictRedis
        #            unit : AdUnit

        key = ''.join(['unit:', str(unit.id)])
        value = ''.join(['{"site":"', str(unit.site.id), '","type":"', unit.type, '","target":"', unit.targetwindow, '"}'])
        #print "pub: ", unit.site.pub
        print 'zadd: key: ', key, ', score: 0, value: ', value
        r.zadd(key, 0, value)
