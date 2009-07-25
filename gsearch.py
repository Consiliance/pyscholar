#!/usr/bin/python
from lxml import etree as et
from urllib import quote_plus,urlopen

def gsearch(q='',num=10,datelimit=''):
        returninfo=[]
        searchurl='http://google.com/search?hl=en&as_q=%s&num=%s&as_qdr=%s'%(quote_plus(q),str(num),datelimit)
        results=urlopen(searchurl).read()
        tree=et.fromstring(results,et.HTMLParser())
        links=tree.xpath('/html/body[@id="gsr"]/div[@id="res"]/div[1]/h3/a')
        return tree
        for a in links:
            returninfo.append({'href':a.values()[0],'text':a.text})
        return returninfo

