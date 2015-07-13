from . import http
import json, urllib.request, urllib.error, urllib.parse, sys


def haste(data):
    URL = "http://paste.dmptr.com"
    request = urllib.request.Request(URL + "/documents", data)
    response = urllib.request.urlopen(request)
    return("%s/%s" % (URL, json.loads(response.read())['key']))


def execute_eval(code, paste_multiline=True):
    while True:
        output = http.get("http://eval.appspot.com/eval", statement=code).rstrip('\n')
        if output:
            break
        else:
            pass

    if "Traceback (most recent call last):" in output:
        status = "Python error: "
    else:
        status = "Code executed sucessfully: "
        
    if "\n" in output and paste_multiline:
        return status + haste(output)
    else:
        return output