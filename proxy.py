import re
import requests
import os.path

import threading
import time

from flask import Flask,request,redirect,Response

#SITE_NAME = "https://www.hpool.com"
#HOST_NAME = "www.hpool.com"

app = Flask(__name__)

print("aaa")


@app.route('/',methods=['GET','POST','DELETE'])
def host():
#    global SITE_NAME
    return proxy("", request)


#@app.route('/')
#def test():
#    print("aaa")
#    return 'runing'


@app.route('/<path:path>',methods=['GET','POST','DELETE'])
def hostpath(path):
    #print(request.url)
#    global SITE_NAME
#    return proxy(f'{SITE_NAME}/{path}', request)
    return proxy(path, request)


def proxy(url, request):
    print("\n%s %s with headers: %s" % (request.method, url, request.headers))
    inheaders = dict(request.headers)
    hostfor = inheaders['X-Forwarded-Host']
    r = make_request(f"https://{hostfor}/{url}", request.method, dict(inheaders), request.form)
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in r.raw.headers.items() if name.lower() not in excluded_headers]
    headers = dict(headers)
    print("Got %s response from %s with headers: %s\n" % (r.status_code, url, headers))
    print("%s\n\n" % (r.content))
    out = Response(r.content, r.status_code, headers)
    return out

#    if request.method=='GET':
#        resp = requests.get(url)
#        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
#        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
#        response = Response(resp.content, resp.status_code, headers)
#        return response
#    elif request.method=='POST':
#        resp = requests.post(url,json=request.get_json())
#        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
#        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
#        response = Response(resp.content, resp.status_code, headers)
#        return response
#    elif request.method=='DELETE':
#        resp = requests.delete(url).content
#        response = Response(resp.content, resp.status_code, headers)
#        return response

def make_request(url, method, headers={}, data=None):
    # Fetch the URL, and stream it back
    headers['Host'] = headers['X-Forwarded-Host']
    del headers['X-Forwarded-For']
    del headers['X-Forwarded-Server']
    del headers['X-Forwarded-Host']
    print("Sending %s %s with headers: %s and data %s\n" % (method, url, headers, data))
    return requests.request(method, url, params=request.args, stream=True, headers=headers, allow_redirects=False, data=data)


if __name__ == "__main__":
    app.run(port=87)
