#!/usr/bin/python
import yaml
import re
import lxml.etree

from BeautifulSoup import BeautifulSoup
#import BSXPath.BSXPathEvaluator, BSXPath.XPathResult
from BSXPath import BSXPathEvaluator, XPathResult
#http://www.crummy.com/software/BeautifulSoup/documentation.html

class Nature(yaml.YAMLObject):
    yaml_tag='!nature'
    def __init__(self):
        pass
    def yaml_repr(self):
        pass
    def __repr__(self):
        return "nature object"
 
class ScienceDirect(yaml.YAMLObject):
    yaml_tag='!sciencedirect'
    def __init__(self):
        pass
    def yaml_repr(self):
        pass
    def __repr__(self):
        return "sciencedirect object"
    def detectWeb(self, doc, url):
        if type(doc) == type(""): 
            doc = BSXPathEvaluator(doc)
        if url.count("_ob=DownloadURL") != 0 or doc.title == "ScienceDirect Login":
            return False
        if ((not re.match("pdf",url)) and url.count("_ob=ArticleURL")==0 and url.count("/article/")==0) or url.count("/journal/") != 0:
            return "multiple"
        elif not re.match("pdf",url):
            return "journalArticle"
        return False
    def doWeb(self, doc, url):
        if type(doc) == type("huh"): #then it's not BeautifulSoup
            tree = lxml.etree.fromstring(doc, lxml.etree.HTMLParser())
            links = tree.xpath("/html/body/div[1]/div/div[@id='sdBody']/div/div[@id='rightCol']/div/div[@id='searchResults']/div[@id='bodyMainResults']")
            #print "links = ", links
            #for each in links:
            #    print type(links[0])
            document = BSXPathEvaluator(doc)
        else: document = doc
        if document.evaluate("//*[contains(@src, \"exportarticle_a.gif\")]", document, None, XPathResult.ANY_TYPE, None):
            articles = []
            if (self.detectWeb(doc, url) == "multiple"):
                #search page
                items = {}
                xpath = None
                if (url.count("_ob=PublicationURL") > 0):
                    xpath = '//table[@class="resultRow"]/tbody/tr/td[2]/a'
                else:
                    xpath = '//div[@class="font3"][@id="bodyMainResults"]/table/tbody/tr/td[2]/a'
                rows = document.evaluate(xpath, document, None, XPathResult.ANY_TYPE, None)
                print rows
                next_row = None
                #for next_row in rows.iterateNext():
                isTrue = True
                next_row = rows
                while isTrue:
                    try: next_row=rows.iterateNext()
                    except IndexError: isTrue=False
                    #while (next_row = rows.iterateNext()):
                    print next_row.__dict__
                    title = "some title here" #next_row.text
                    link = "some href here" #next_row.href
                    if not re.match("PDF \(",title) and not re.match("Related Articles",title): items[link] = title;
                #items = zotero.SelectItems(items)
                #let's assume we want all of them
                [articles.append(i) for i in items]
                result_sets = []
                for article in articles:
                    result_sets.append({'article':article})
            else:
                articles = [url]
                return_sets = [{"currentdoc":doc}]
            if len(articles) == 0:
                print "ERROR: no items were found"
                return
            print "articles = ", articles
            print "result_sets = ", result_sets
        return result_sets #return all articles or the currentdoc in a dict for stuff that we want to grab

