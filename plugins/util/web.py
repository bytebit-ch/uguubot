""" web.py - handy functions for web services """

from . import http
from . import urlnorm
import json
import urllib.request, urllib.parse, urllib.error
import myql

short_url = "http://is.gd/create.php"
paste_url = "http://hastebin.com"

YQL = myql.MYQL()

class ShortenError(Exception):
    def __init__(self, code, text):
        self.code = code
        self.text = text

    def __str__(self):
        return self.text


def isgd(url):
    """ shortens a URL with the is.gd API """
    url = urlnorm.normalize(url, assume_scheme='http')
    params = urllib.parse.urlencode({'format': 'json', 'url': url})
    request = http.get_json("http://is.gd/create.php?%s" % params)

    if "errorcode" in request:
        raise ShortenError(request["errorcode"], request["errormessage"])
    else:
        return request["shorturl"]


def try_isgd(url):
    try:
        out = isgd(url)
    except (ShortenError, http.HTTPError):
        out = url
    return out


def haste(text, ext='txt'):
    """ pastes text to a hastebin server """
    page = http.get(paste_url + "/documents", post_data=text)
    data = json.loads(page)
    return ("%s/%s.%s" % (paste_url, data['key'], ext))


class YqlResult:
    def __init__(self, obj):
        self.obj = obj

    def one(self):
        keys = list(self.obj["query"]["results"].keys())
        if len(keys) != 1:
            return {}

        return self.obj["query"]["results"][keys[0]]


def query(query, params={}):
    """ runs a YQL query and returns the results """
    for k, v in params.items():
        query = query.replace("@" + k, "'" + v + "'")

    print(query)

    return YqlResult(YQL.rawQuery(query).json())
