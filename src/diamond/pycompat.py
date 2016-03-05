# coding=utf-8
URLOPEN = "diamond.pycompat.urlopen"
try:
    from urllib2 import HTTPError, Request, urlopen, URLError
    from urllib import urlencode, quote
    from urlparse import urljoin, urlparse
    from Queue import Empty, Full, Queue
except ImportError:
    from urllib.request import HTTPError, Request, URLError, urlopen
    from urllib.parse import urlencode, quote, urljoin, urlparse
    from queue import Full, Empty, Queue

try:
    unicode = unicode
except NameError:
    unicode = str
