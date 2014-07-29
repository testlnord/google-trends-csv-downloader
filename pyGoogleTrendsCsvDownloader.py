import httplib
import urllib
import urllib2
import re
import csv
import lxml.etree as etree
import lxml.html as html
import traceback
import gzip
import random
import time
import sys
import random

from cookielib import Cookie, CookieJar
from StringIO import StringIO


class QuotaExceededException(Exception):
    pass

class pyGoogleTrendsCsvDownloader(object):
    '''
    Google Trends Downloader.

    Recommended usage:

    from pyGoogleTrendsCsvDownloader import pyGoogleTrendsCsvDownloader
    r = pyGoogleTrendsCsvDownloader(username, password)
    r.get_csv_data(cat='0-958', geo='US-ME-500')

    '''
    def __init__(self, username, password):
        '''
        Provide login and password to be used to connect to Google Trends
        All immutable system variables are also defined here
        '''

        # The amount of time (in secs) that the script should wait before making a request.
        # This can be used to throttle the downloading speed to avoid hitting servers too hard.
        # It is further randomized.
        self.download_delay = 2

        self.service = "trendspro"
        self.url_service = "http://www.google.com/trends/"
        self.url_download = 'https://www.google.com/trends/trendsReport?'

        self.login_params = {}
        # These headers are necessary, otherwise Google will flag the request at your account level
        self.headers = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'),
                        ("accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
                        ("Accept-Language", "en-gb,en;q=0.8"),
                        ("Accept-Encoding", "gzip,deflate,sdch"),
                        ("referer", "https://www.google.com/trends/explore"),
                        ("pragma", "no-cache"),
                        ("cache-control", "no-cache"),
                        ]
        self.url_login = 'https://accounts.google.com/ServiceLogin?service='+self.service+'&passive=1209600&continue='+self.url_service+'&followup='+self.url_service
        self.url_authenticate = 'https://accounts.google.com/accounts/ServiceLoginAuth'

        self._authenticate(username, password)

    def _authenticate(self, username, password):
        '''
        Authenticate to Google:
        1 - make a GET request to the Login webpage so we can get the login form
        2 - make a POST request with email, password and login form input values
        '''
        # Make sure we get CSV results in English
        ck1 = Cookie(version=0, name='I4SUserLocale', value='en_US', port=None, port_specified=False, domain='.google.com', domain_specified=False,domain_initial_dot=False, path='', path_specified=False, secure=False, expires=None, discard=False, comment=None, comment_url=None, rest=None)
        # This cookie is now mandatory
        # Not sure what the value represents but too many queries from the same value
        # lead to a Quota Exceeded error.
        # random_six_char = ''.join(random.choice('0123456789abcdef') for n in xrange(6))
        ck2 = Cookie(version=0, name='PREF', value='0000', port=None, port_specified=False, domain='.google.com', domain_specified=False,domain_initial_dot=False, path='', path_specified=False, secure=False, expires=None, discard=False, comment=None, comment_url=None, rest=None)

        self.cj = CookieJar()
        self.cj.set_cookie(ck1)
        self.cj.set_cookie(ck2)

        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        self.opener.addheaders = self.headers

        # Get all of the login form input values
        find_inputs = etree.XPath("//form[@id='gaia_loginform']//input")
        resp = self.opener.open(self.url_login)
        data = self.read_gzipped_response(resp)

        try:
            xmlTree = etree.fromstring(data, parser=html.HTMLParser(recover=True, remove_comments=True))
            for input in find_inputs(xmlTree):
                name = input.get('name')
                if name:
                    name = name.encode('utf8')
                    value = input.get('value', '').encode('utf8')
                    self.login_params[name] = value
        except:
            print("Exception while parsing: %s\n" % traceback.format_exc())

        self.login_params["Email"] = username
        self.login_params["Passwd"] = password

        params = urllib.urlencode(self.login_params)
        auth_resp = self.opener.open(self.url_authenticate, params)

        # Testing whether Authentication was a success
        # I noticed that a correct auth sets a few cookies
        if not self.is_authentication_successfull(auth_resp):
            print 'Warning: Authentication failed for user %s' % username
        else:
            print 'Authentication successfull for user %s' % username

    def is_authentication_successfull(self, response):
        '''
            Arbitrary way of us knowing whether the authentication succeeded or not:
            we look for a SSID cookie-set header value.
            I noticed that the 4 mandatory cookies were:
              - SID
              - SSID
              - HSID
              - PREF (but does not need to be set)
        '''
        if response:
            return 'SSID' in response.info().getheader('Set-Cookie')

        return False

    def is_quota_exceeded(self, response):
        # TODO: double check that the check for the content-disposition
        # is correct
        if response.info().has_key('Content-Disposition'):
            return False
        return True

    def read_gzipped_response(self, response):
        '''
            Since we are adding gzip to our http request Google can answer with gzipped data
            that needs uncompressing before handling.
            This method returns the text content of a Http response.
        '''
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(response.read())
            f = gzip.GzipFile(fileobj=buf)
            content = f.read()
        else:
            content = response.read()
        return content

    def get_csv_data(self, **kwargs):
        '''
        Download CSV reports
        '''
        time.sleep(self.download_delay)

        params = {
            'hl': 'en-us',
            'export': 1
        }
        params.update(kwargs)

        # Silly python with the urlencode method
        params = urllib.urlencode(params).replace("+", "%20")
        response = self.opener.open(self.url_download + params)

        # Make sure quotas are not exceeded ;)
        if self.is_quota_exceeded(response):
           raise QuotaExceededException()

        return self.read_gzipped_response(response)

