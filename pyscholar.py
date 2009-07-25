#!/usr/bin/python

import copy
import re
import httplib
import urllib
from BeautifulSoup import BeautifulSoup

SEARCH_HOST = "scholar.google.com"
SEARCH_BASE_URL = "/scholar"
terms = ["PDMS"]
limit = 10 #100

params = urllib.urlencode({'q': "+".join(terms), 'num':limit})
headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US    ; rv:1.9.0.9) Gecko/2009050519 Iceweasel/3.0.6 (Debian-3.0.6-1)'}
url = SEARCH_BASE_URL + "?" + params

#conn = httplib.HTTPConnection(SEARCH_HOST)
#conn.request("GET", url, {}, headers)
#resp = conn.getresponse()
status = 200#resp.status

if status==200:
    #html = resp.read()
    file2 = open("scholar.htm","r")
    html = file2.read()
    file2.close()
    results = []
    html = html.decode('ascii', 'ignore')
    soup = BeautifulSoup(html)
    for record in soup('p'):
        blah = record.find(name=re.compile("h3"))
        blah2 = record.find(name=re.compile("form"))
        if not blah == None and blah2 == None:
            #continue
           print "record = ", record 
