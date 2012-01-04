from tgen.requester import Requester, ttypes as o

import requests
from lib.helpers import fixurl
from time import time, sleep

from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport

from hashlib import sha1
from redis import Redis
import memcache
from urlparse import urlparse

from lib.ratelimiter import RateLimiter

class RequestHandler(object):
    def __init__(self):
        pass

    def urlopen(self, request):
        """
        returns a response for the request
        """
        raise NotImplementedError

    def cache_urlopen(self, request):
        """
        returns a response if it's in the cache
        """
        raise NotImplementedError

    def set_cache(self, request, response):
        """
        updates the cache w/ the given response
        """
        raise NotImplementedError

    def live_urlopen(self, request):
        """
        makes request to host and returns response
        """
        raise NotImplementedError

    def check_rate_allowed(self, request):
        """
        returns the rate you are allowed to pull data from
        the host at
        """
        raise NotImplementedError

    def update_rate(self, response):
        """
        updates our rate counter based on the response
        """
        raise NotImplementedError

class LiveRequestHandler(RequestHandler):

    timeout = 30

    def urlopen(self,request):
        return self.live_urlopen(request)

    def live_urlopen(self, request):
        s = time()

        method = request.method or 'get'
        try:
            getter = getattr(requests,method)
        except AttributeError, ex:
            raise o.Exception('Bad method: %s' % method)

        try:
            # use the requests getter to get the resource
            http_response = getter(request.url,
                                   cookies=request.cookies,
                                   timeout=self.timeout,
                                   # don't just get headers
                                   prefetch=True,
                                   # we want raw data, not unicode
                                   config={'decode_unicode':False})
        except Exception, ex:
            # problem actually trying to get the resource
            raise o.Exception('HTTP Request Error: %s' % ex)

        # build our response obj / aka copy that shit
        response = o.Response()
        response.status_code = http_response.status_code
        response.url = fixurl(http_response.url)
        response.headers = http_response.headers
        response.content = http_response.content
        response.timestamp = time()
        response.response_time = (time() - s)

        # and we're done!
        return response

class CachingRequestHandler(RequestHandler):
    def __init__(self,memcached_host='127.0.0.1',memcached_port=11211):
        self.memcached_host = memcached_host
        self.memcached_port = memcached_port
        self.mc = memcache.Client(['%s:%s' %
                            (self.memcached_host,self.memcached_port)])
        self.pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    def urlopen(self,request):
        return self.cached_urlopen(request)

    def cache_urlopen(self,request):
        # check the cache
        cache_key = self.get_cache_key(request)
        print 'getting: %s' % cache_key
        cache_response = self.mc.get(cache_key)

        # no cache hit?
        if not cache_response:
            return None # TODO: see if i can even do this

        print 'got: %s' % len(cache_response)

        # deserialize our response
        response = self._deserialize_o(o.Response,cache_response)
        response.from_cache = True
        return response

    def set_cache(self,request,response):
        """ caches the response for a request """
        url = request.url
        cache_key = self.get_cache_key(request)
        data = self._serialize_o(response)
        self.mc.set(cache_key,data)
        return True

    def get_cache_key(self,request):
        """ returns the key for the given request in the cache """
        return 'httpcache:%s' % sha1(request.url).hexdigest()

    def _serialize_o(self, obj):
        trans = TTransport.TMemoryBuffer()
        prot = self.pfactory.getProtocol(trans)
        obj.write(prot)
        return trans.getvalue()

    def _deserialize_o(self, objtype, data):
        print 'deserialize: %s' % len(data)
        prot = self.pfactory.getProtocol(TTransport.TMemoryBuffer(data))
        ret = objtype()
        ret.read(prot)
        return ret

class RateLimitingRequestHandler(RequestHandler):

    def __init__(self, redis_host='127.0.0.1',
                       max_data_rate=(
                           1024 * 1024 * 1, # 1MB
                           10)): # per N seconds

        self.redis_host = redis_host
        self.rc = Redis(self.redis_host)

        # based on bytes / s
        self.max_data_rate = max_data_rate

        # our limiter
        self.rl = RateLimiter(
            self.rc, 'httplimiter',
            max_data_rate[0] * 2, # span
            float(max_data_rate[1]) / 10 # grainularity
        )

    def check_rate_allowed(self, request):
        """
        returns False if we have already passed the limit
        for the given site. We are limiting our rate to
        a given MB/s
        """

        size, seconds = self.max_data_rate
        root = self._get_url_root(request)
        count = self.rl.count(root,seconds)
        # we are going to return the max # of bytes
        return size - count

    def update_rate(self, response):
        """
        updates the rate tracking info based on the response
        """
        root = self._get_url_root(response)
        self.rl.add(root,len(response.content)) # bytes

    def _get_url_root(self, response):
        return urlparse(response.url).netloc

class MatureRequestHandler(CachingRequestHandler,
                           LiveRequestHandler,
                           RateLimitingRequestHandler):

    def __init__(self, redis_host=None,
                       memcache_host=None,
                       memcache_port=None,
                       max_data_rate=None):

        # initialize the lil ppl
        args = [x for x in [memcache_host,memcache_port] if x]
        CachingRequestHandler.__init__(self,*args)

        args = [x for x in [redis_host,max_data_rate] if x]
        RateLimitingRequestHandler.__init__(self,*args)


    def urlopen(self, request):
        print 'urlopen: %s' % request.url

        response = None

        if not request.no_cache:
            # check the cache
            response = self.cache_urlopen(request)
            if response:
                print 'response from cache: %s' % request.url

        # check and make sure we aren't going to have
        # to fail due to rate limiting for the site
        # this should return the rate at which we can
        # pull data.
        if not response:
            self.wait_for_allowed(request)

        # make our request
        if not response:
            response = self.live_urlopen(request)
            print 'live response: %s' % request.url
            # update the cache
            self.set_cache(request,response)

        # update the rate limiter
        self.update_rate(response)

        # return the response
        print 'returning urlopen: %s' % request.url
        return response

    def wait_for_allowed(self, request):
        allowed_rate = self.check_rate_allowed(request)
        print 'allow rate: %s' % allowed_rate
        while allowed_rate < 1:
            sleep(1)
            allowed_rate = self.check_rate_allowed(request)
            print 'allow rate: %s' % allowed_rate
        return True


def run():
    from run_services import serve_service
    serve_service(Requester, MatureRequestHandler())

if __name__ == '__main__':
    run()
