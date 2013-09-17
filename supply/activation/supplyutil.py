# classes used: AdUnit
#               redis.StrictRedis

class SupplyUtil:

    @staticmethod
    def pushUnit(r, unit):
        # arguments: r : redis.StrictRedis
        #            unit : AdUnit

        key = ''.join(['unit:', unit.name])
        value = ''.join(['{"site":"', str(unit.site.id), '","type":"', unit.type, '","target":"', unit.targetwindow, '"}'])
        #print "pub: ", unit.site.pub
        print 'key: ', key, ', value: ', value
        r.zadd(key, 0, value)
