"""
scHolar index
http://insitu.lri.fr/~roussel/moulinette/h/h.cgi

The following Python code makes it possible to compute H indices by
using Beautiful Soup to process Google Scholar results.

This code is in the public domain.

For more information, see:
   http://en.wikipedia.org/wiki/Hirsch_number
   http://scholar.google.com/
   http://www.crummy.com/software/BeautifulSoup/

Comments and questions should be sent to Nicolas Roussel (roussel@lri.fr).
"""

import os, sys, socket, re, string
import BeautifulSoup

def debugInfo(text):
    print text
    sys.stdout.flush()

# ------------------------------------------------------------------------------

class GoogleScholarReference:

    def getURL(self):
        if self.gid==None: return None
        return "http://scholar.google.com/scholar?cluster=%s"%self.gid

    def getCitedByURL(self):
        if self.gid==None: return None
        return "http://scholar.google.com/scholar?cites=%s"%self.gid

    def get(self, key, defval=None):
        if self.__dict__.has_key(key): return self.__dict__[key]
        return defval

_citedby = re.compile('.*Cited by (\d+).*')
_pubyear = re.compile('.*\D(\d\d\d\d)\D.*')
_id_cites = re.compile('.*cites=(\d+).*')
_id_cluster = re.compile('.*cluster=(\d+).*')

def _deHTML(line, group):
    text = re.sub("&nbsp;"," ",line)
    text = re.sub("<[^<]+>","",text)
    if group:
        #text = re.sub("- group of.+","",text)
        text = re.sub("- all .+","",text)
    return text.strip()
        
def _splitDescription(reference):
    reftext = unicode(reference)
    text = reftext.replace("\n"," ")
    text = re.sub("<p[^>]*>","",text)
    text = re.sub("</p>","",text)
    text = re.sub("<font[^>]*>","",text)
    text = re.sub("</font>","",text)
    #text = re.sub("<b>\[.+\]</b>","",text)
    text = re.sub("<b>\[.+\]</b>","",text)
    return text.split("<br />")

def _tryExp(text,exp,defval):
    m = exp.match(text)
    if m: return m.group(1)
    return defval

#dbgfile = open("/tmp/text.txt","w")
def _parseResults(soup):
    result = []
    reference = soup.first('p', {'class':'g'})
    while reference!=None:
        try:
            r = GoogleScholarReference()
            d = _splitDescription(reference)
            r.title = _deHTML(d[0],True)
            r.info = _deHTML(d[1],False)
            r.citedby = int(_tryExp(d[-1],_citedby,0))
            r.year = int(_tryExp(d[1],_pubyear,0))
            r.gid = _tryExp(d[-1],_id_cites,None)
            if not r.gid: r.gid = _tryExp(d[-1],_id_cluster,None)
            result.append(r)
        except:
            #dbgfile.write("\n-----------------------\n")
            #dbgfile.write("%s"%d)
            pass
        reference = reference.nextSibling
    return result

# ------------------------------------------------------------------------------

_qServer,_qPort,_qTimeout = "scholar.google.com",80,5.0
_qTemplate = "/scholar?num=%d&"
   
def doQuery(query):
    refs, offset, inc = [], 0, 100
    while True:
        q = _qTemplate%inc+query
        if offset==0:
            debugInfo(u'Sending <a href="http://%s%s">query</a> to Google Scholar...'%(_qServer,q))
        else:
            q = q+"&start=%d"%offset
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(_qTimeout)
        try:
            err = sock.connect_ex((_qServer, _qPort))
        except socket.gaierror:
            debugInfo(u"unable to connect")
            return []
        if err!=0:
            debugInfo(u"connection timed out (%s seconds)..."%_qTimeout)
            return []
        sock.send("GET %s HTTP/1.1\n"%q)
        sock.send("Host: scholar.google.com\n")
        sock.send("Connection: close\n") # since we don't parse the HTTP response
        sock.send("Referer: http://scholar.google.com/advanced_scholar_search?hl=en&lr=\n")
        sock.send("User-Agent: %s\n"%os.environ.get("HTTP_USER_AGENT","Mozilla/5.0"))
        sock.send("\n")
        print "query = ", q
        debugInfo("reading...")
        data = ""
        while True:
            moredata = sock.recv(4096)
            if not moredata: break
            data = data+moredata
        sock.close()
        open("/tmp/scholar-results.html","w").write(data)
        debugInfo("parsing...")
        soup = BeautifulSoup.BeautifulSoup(data)
        morerefs = _parseResults(soup)
        refs = refs + morerefs
        if len(morerefs)!=inc:
            if len(morerefs)==0:
                location = None
                for line in string.split(data,"\n"):
                    if line.find("Location: ")!=-1:
                        location  = string.split(line)[-1]
                        break
                message = "query failed..."
                if location:
                    #message = message + ' (try again after a while or after solving <a href="%s">this</a>)'%location
                    message = message + ' (try again after a while)'
                elif len(refs)!=0:
                    message = message + ' (try again after a while)'
                debugInfo(message)
            break
        offset = offset+inc
    return refs

def fakeQuery(filename):
    debugInfo(u'Opening %s...'%os.path.basename(filename))
    data = open(filename).read()
    soup = BeautifulSoup.BeautifulSoup(data)
    references = _parseResults(soup)
    return references

# ------------------------------------------------------------------------------

def computeHindex(references):
    h = 0
    while True:
        h = h + 1
        n = 0
        for r in references:
            if r.citedby>=h: n = n+1
        if n<h: return h-1

# ------------------------------------------------------------------------------

if __name__=="__main__":
    name = sys.argv[1]
    name = name.replace(" ","+")
    name = name.replace('"',"%22")
    references = doQuery("as_sauthors=%s"%name)
    print "scHolar index:", computeHindex(references)

