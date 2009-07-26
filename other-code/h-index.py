#!/usr/bin/python

import httplib, urllib, re, sys
from BeautifulSoup import BeautifulSoup

terms = sys.argv[1:]
limit = 100
params = urllib.urlencode( { 'q': "+".join( terms ), 'num': limit } )
headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; WindowsNT)'}
url = '/scholar'+"?"+params
conn = httplib.HTTPConnection( 'scholar.google.com' )
conn.request( "GET", url, {}, headers )

resp = conn.getresponse()
cites = []
if resp.status == 200:
    html = resp.read()
    html = html.decode( 'ascii', 'ignore' )
    soup = BeautifulSoup( html )
    for record in soup( 'h3', { 'class': 'r' } ):
        print "we have a match!"
        match = re.search("Cited by ([^<]*)", str(record))
        if match != None:
            cite = int( match.group( 1 ) )
            cites.append( cite )
else:
    print 'Error: '
    print resp.status, resp.reason

cites.sort()
cites.reverse()

h = 0
for cite in cites:
    if cite > h:
        h += 1
print h

