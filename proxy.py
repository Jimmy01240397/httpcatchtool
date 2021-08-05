import re
import requests
import os.path

import threading
import time

from flask import Flask,request,redirect,Response

app = Flask(__name__)

print("aaa")


@app.route('/',methods=['GET','POST','DELETE'])
def host():
    return proxy("", request)

@app.route('/<path:path>',methods=['GET','POST','DELETE'])
def hostpath(path):
    return proxy(path, request)


def proxy(url, request):
    print("\n%s %s with headers: %s" % (request.method, url, request.headers))
    inheaders = dict(request.headers)
    hostfor = inheaders['Host']
    r = make_request(f"https://{hostfor}/{url}", request.method, dict(inheaders), request.form)
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in r.raw.headers.items() if name.lower() not in excluded_headers]
    headers = dict(headers)
    print("Got %s response from %s with headers: %s\n" % (r.status_code, url, headers))
    print("%s\n\n" % (r.content))
    out = Response(r.content, r.status_code, headers)
    return out

def make_request(url, method, headers={}, data=None):
    # Fetch the URL, and stream it back
    if method == 'POST':
        if headers['Content-Type'] == 'application/json':
            print("Sending %s %s with headers: %s and data %s\n" % (method, url, headers, request.get_data()))
            return requests.request(method, url, params=request.args, stream=True, headers=headers, allow_redirects=False, json=json.loads(request.get_data()))
    print("Sending %s %s with headers: %s and data %s\n" % (method, url, headers, data))
    return requests.request(method, url, params=request.args, stream=True, headers=headers, allow_redirects=False, data=data)


if __name__ == "__main__":
    app.run(port=87)
