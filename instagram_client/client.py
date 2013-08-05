import requests, urllib
import time
import hashlib, hmac
import json
import mimetypes
import sys
from collections import OrderedDict
    
    
class Service:
    KEY = "" # do NOT ask me for the key
    KEY_VERSION = "4"
    USERAGENT = "Instagram 4.0.2 (iPad2,5; iPhone OS 6_1; en_US; en) AppleWebKit/420+"
    BOUNDARY = "Boundary+0xAbCdEfGbOuNdArY"
    DEVICEID = "00000000-0000-0000-0000-000000000000"
    
    def __init__(self):
        self.cookies = {}
        if not self.__class__.KEY:
            print "*** KEY is missing *** (do NOT ask me for the key)"
            sys.exit(1)

    def call(self, method, url, *args, **kwargs):
        kwargs['headers'] = dict({
            "User-Agent": self.__class__.USERAGENT,
            "Accept": "*/*",
            "Accept-Language": "en",
            "Connection": "keep-alive"
        }, **kwargs.get('headers', {}))
        kwargs['cookies'] = dict(self.cookies, **kwargs.get('cookies', {}))
        kwargs['proxies'] = urllib.getproxies() # for debugging
        
        if kwargs.pop("signed", False):
            kwargs['headers']['Content-Type'], kwargs['data'] = self.__class__.signedPostParameters(kwargs.get('data', {}))
        
        print method, url, kwargs
        methodToCall = getattr(requests, method)
        r = methodToCall(url, **kwargs)
        self.keepCookies(r)
        return r
    
    def keepCookies(self, r):
        for h in r.history:
            self.cookies.update(h.cookies)
        self.cookies.update(r.cookies)
    
    @classmethod
    def signedPostParameters(cls, parameters):
        j = json.dumps(parameters, sort_keys=False, separators=(',',':'))
        signed_body = "%s.%s" % (cls.HMACWithSecret(j), j)
        return cls.encode_multipart_formdata({
            'signed_body': signed_body,
            'ig_sig_key_version': cls.KEY_VERSION
        })
    
    @classmethod
    def HMACWithSecret(cls, string):
        return hmac.new(cls.KEY, string, hashlib.sha256).hexdigest()
    
    @classmethod
    def encode_multipart_formdata(cls, fields, files={}):
            BOUNDARY = cls.BOUNDARY
            CRLF = '\r\n'
            L = []
            for key, value in sorted(fields.items(), reverse=True):
                L.append('--' + BOUNDARY)
                L.append('Content-Disposition: form-data; name="%s"' % key)
                L.append('')
                L.append(value)
            for (key, filename, value) in files.iteritems():
                L.append('--' + BOUNDARY)
                L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
                L.append('Content-Type: %s' % cls.get_content_type(filename))
                L.append('')
                L.append(value)
            L.append('--' + BOUNDARY + '--')
            L.append('')
            body = CRLF.join(L)
            content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
            return content_type, body
    
    @classmethod
    def get_content_type(cls, filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


class Instagram(Service):
    
    def login(self, username, password):
        r = self.call("post",
                      "https://instagram.com/api/v1/accounts/login/",
                      signed = True,
                      data = OrderedDict([
                          ("_uuid", self.__class__.DEVICEID),
                          ("password", password),
                          ("username", username),
                          ("device_id", self.__class__.DEVICEID),
                          ("_csrftoken", "missing")
                      ])
        )
        print r.text
        
    def upload(self, filename):
        r = self.call("post",
                      "http://instagram.com/api/v1/media/upload/",
                      files = {
                          'photo': open(filename, 'rb')
                      },
                      data = {
                          'device_timestamp': int(time.time())
                      }
        )
        print r.text
        return r.json()["media_id"]
        
    def configure(self, media_id, caption):
        r = self.call("post",
                      "https://instagram.com/api/v1/media/configure/",
                      signed = True,
                      cookies = {
                          "igls": self.cookies["ds_user"]
                      },
                      data = OrderedDict([
                          ("device_timestamp", int(time.time())),
                          ("media_id", media_id),
                          ("caption", caption),
                          ("_uid", self.cookies["ds_user_id"]),
                          ("_csrftoken", self.cookies["csrftoken"]),
                          ("_uuid", self.__class__.DEVICEID),
                          ("geotag_enabled", False),
                          ("usertags", '{"in":[]}'),
                          ("source_type", 0)
                      ])
        )
        print r.text
        
        
