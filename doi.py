#!/usr/bin/python
#author: Bryan Bishop <kanzure@gmail.com>
#date: 2010-03-04
#purpose: resolve a pesky DOI number
import urllib2, httplib
import optfunc
httplib.HTTPConnection.debuglevel = 1

user_agent = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.5) Gecko/20091123 Iceweasel/3.5.5 (like Firefox/3.5.5; Debian-3.5.5-1)"

def doi(number):
    '''resolves a DOI number, like: 10.1038/nature01036'''

    request = urllib2.Request("http://dx.doi.org/%s" % (number))
    opener = urllib2.build_opener()
    f = opener.open(request)
    print f.url, "\n"

if __name__ == "__main__":
    optfunc.run(doi)
