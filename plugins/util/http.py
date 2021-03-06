# convenience wrapper for urllib2 & friends

import http.cookiejar
import json
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import urllib.parse
import re
from urllib.parse import quote, quote_plus as _quote_plus

from lxml import etree, html
from bs4 import BeautifulSoup
from urllib.error import URLError, HTTPError

ua_firefox = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/17.0' \
             ' Firefox/17.0'
ua_old_firefox = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; ' \
    'rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6'
ua_internetexplorer = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
ua_chrome = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.4 (KHTML, ' \
            'like Gecko) Chrome/22.0.1229.79 Safari/537.4'

jar = http.cookiejar.CookieJar()


def get(*args, **kwargs):
    return open(*args, **kwargs).read().decode("utf-8")


def get_url(*args, **kwargs):
    return open(*args, **kwargs).geturl()


def get_html(*args, **kwargs):
    return html.fromstring(get(*args, **kwargs))


def get_soup(*args, **kwargs):
    return BeautifulSoup(get(*args, **kwargs), 'lxml')


def get_xml(*args, **kwargs):
    return etree.fromstring(get(*args, **kwargs))


def get_json(*args, **kwargs):
    return json.loads(get(*args, **kwargs))


def open(url, query_params=None, user_agent=None, post_data=None,
         referer=None, get_method=None, cookies=False, **kwargs):

    if query_params is None:
        query_params = {}

    if user_agent is None:
        user_agent = ua_firefox

    query_params.update(kwargs)

    url = prepare_url(url, query_params)

    request = urllib.request.Request(url, post_data)

    if get_method is not None:
        request.get_method = lambda: get_method

    request.add_header('User-Agent', user_agent)

    if referer is not None:
        request.add_header('Referer', referer)

    if cookies:
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    else:
        opener = urllib.request.build_opener()

    return opener.open(request)


def prepare_url(url, queries):
    if queries:
        scheme, netloc, path, query, fragment = urllib.parse.urlsplit(url)

        query = dict(urllib.parse.parse_qsl(query))
        query.update(queries)
        query = urllib.parse.urlencode(dict((to_utf8(key), to_utf8(value))
                                  for key, value in query.items()))

        url = urllib.parse.urlunsplit((scheme, netloc, path, query, fragment))

    return url


def to_utf8(s):
    if isinstance(s, str):
        return s.encode('utf8', 'ignore')
    else:
        return str(s)

# def quote(s):
#     return urllib.quote(s)

def quote_plus(s):
    return _quote_plus(to_utf8(s))

def unquote(s):
    return urllib.parse.unquote(s)

def unescape(s):
    if not s.strip():
        return s
    return html.fromstring(s).text_content()

def strip_html(html):
    tag = False
    quote = False
    out = ""

    for c in html:
        if c == '<' and not quote: tag = True
        elif c == '>' and not quote: tag = False
        elif (c == '"' or c == "'") and tag: quote = not quote
        elif not tag: out = out + c

    return out

def decode_html(string):
    import re
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")

    def substitute_entity(match):
        from html.entities import name2codepoint as n2cp
        ent = match.group(2)
        if match.group(1) == "#":
            return chr(int(ent))
        else:
            cp = n2cp.get(ent)
            if cp:
                return chr(cp)
            else:
                return match.group()

    return entity_re.subn(substitute_entity, string)[0]


def clean_html(string):
    import html.parser
    h = html.parser.HTMLParser()
    return h.unescape(string)

    #clean up html chars
    #out = HTMLParser.HTMLParser().unescape(out)
    #out = out.replace("&amp;","&").replace("&quot;",'"').replace('&#039;',"'").replace("&lt;","<").replace("&gt;",">").replace("&#8211;","-").replace('&#47;','/')

#.renderContents().strip().decode('utf-8').replace('<br/>', '  ')
#    post = re.sub('[\s]{3,}','  ',post) #remove multiple spaces
def process_text(string):
    try: string = string.replace('<br/>','  ').replace('\n','  ')
    except: pass
    string = re.sub('&gt;&gt;\d*[\s]','',string) #remove quoted posts
    string = re.sub('(&gt;&gt;\d*)','',string)
    try: string = str(string, "utf8")
    except: pass
    try: string = strip_html(string)
    except: pass
    try: string = decode_html(string)
    except: pass
    try: string = string.decode('utf-8').strip()
    except: pass
    string = re.sub('[\s]{3,}','  ',string)
    return string

def is_active(url):
    try:
        f = urllib.request.urlopen(urllib.request.Request(url))
        return True
    except:
        return False


def get_element(soup,element,idclass=None,selector=None):
    if idclass: result = soup.find(element, {idclass: selector}).renderContents().strip()
    else: result = soup.find(element).renderContents().strip()
    return process_text(result)


# while u',,' in page:
#         page = page.replace(u',,', u',"",')
