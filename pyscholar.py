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
            #process one of the results
            #print "record = ", record
            paper_title = ""
            journal_href = "" #link to something like sciencedirect
            for stuff in record('a'):
                if stuff._getAttrMap().has_key("onmousedown") and not stuff._getAttrMap().has_key("class"):
                    paper_title = stuff.renderContents()
                    journal_href = stuff._getAttrMap()["href"]
                    #print "title = ", paper_title
                    #print "href = ", href
                elif stuff._getAttrMap().has_key("onmousedown"): #but it has a class
                    #print "it has a class and is onmousedown .. ";
                    #print stuff.renderContents()
                    href = stuff._getAttrMap()["href"]
                    link_title = stuff.renderContents()
                    if not link_title == "BL Direct": #then it might be useful.
                        if href[-3:] == "pdf":
                            #TODO: add to record object as potential PDF link
                            pass
                        else:
                            print "ERROR: what do I want to do with this? href = ", href
                else: #it does not have onmousedown nor has a class in the link. what is it?
                    #cites or cluster
                    href = stuff._getAttrMap()["href"]
                    if href.count("cites") > 0: #Cited by this-many
                        #ISI Web of Knowledge integration? Nah.
                        cites_link = href
                        cites_link_name = stuff.renderContents()
                        #TODO: add to record object
                    elif href.count("cluster") > 0: #All x versions
                        cluster_link = href
                        cluster_link_name = stuff.renderContents()
                        #TODO: parse number of papers that have cited this paper
                        #TODO: add to record object
                    elif href.count("related") > 0: #related articles
                        related_link = href
                        related_link_name = stuff.renderContents()
                        #TODO: add to record object
                    elif stuff.renderContents() == "View as HTML":
                        view_as_html_link = href
                        #TODO: add to record object
                    else: 
                        print "ERROR: was not a citation nor a 'see all versions' nor a related-papers link"
                        print "title was = ", stuff.renderContents()
            #grab description
            #print "record = ", record
            for more in record('font',{'size':'-1'}):
                #print "more = ", more.renderContents()
                #grab authors
                author_data = ""
                for jiggie in more('span',{'class':'a'}):
                    content = jiggie.renderContents()
                    content_array = content.split(" - ")
                    author_data = content_array[0]
                    #strip bold tags from author_data
                    #i don't know how to do this with BeautifulSoup
                    author_data = ''.join(BeautifulSoup(author_data).findAll(text=True))
                    author_data = author_data.replace("&hellip;","") #replace ellipses
                    authors = author_data.split(",")
                    publication = content_array[1]
                    #last four digits should be a year
                    pub_year = content_array[1][-4:]
                    if len(content_array) > 2:
                        server = content_array[2]
                        #print "server = ", server
                    #print "authors = ", author_data
                    #print "publisher = ", publication
                    #print "publication year = ", pub_year
                    
            #what now?

