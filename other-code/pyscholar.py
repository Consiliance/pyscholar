#!/usr/bin/python

import copy
import re
import sys
import yaml
import httplib
import urllib
from BeautifulSoup import BeautifulSoup

if len(sys.argv) == 0: exit()

class Paper(yaml.YAMLObject):
    yaml_tag='!paper'
    def __init__(self, title="paper title goes here", journal_href="http://google.com/", potential_PDF_link="", cites_link="", cites_link_name="", diff_versions_link="", diff_versions_link_name="", related_papers_link="", view_as_html_link="", authors=[], publication="", pub_year="0001", server=""):
        self.title, self.journal_href, self.potential_PDF_link, self.cites_link, self.cites_link_name, self.diff_versions_link, self.diff_versions_link_name, self.related_papers_link, self.view_as_html_link, self.authors, self.publication, self.pub_year, self.server = title, journal_href, potential_PDF_link, cites_link, cites_link_name, diff_versions_link, diff_versions_link_name, related_papers_link, view_as_html_link, authors, publication, pub_year, server
    def __repr__(self):
        return "Paper(title=\"%s\", journal_href=\"%s\", potential_PDF_link=\"%s\", cites_link=\"%s\", cites_link_name=\"%s\", diff_versions_link=\"%s\", diff_versions_link_name=\"%s\", related_papers_link=\"%s\", view_as_html_link=\"%s\", authors=\"%s\", publication=\"%s\", pub_year=\"%s\", server=\"%s\")" % (self.title, self.journal_href, self.potential_PDF_link, self.cites_link, self.cites_link_name, self.diff_versions_link, self.diff_versions_link_name, self.related_papers_link, self.view_as_html_link, self.authors, self.publication, self.pub_year, self.server) 

SEARCH_HOST = "scholar.google.com"
SEARCH_BASE_URL = "/scholar"
terms = [sys.argv[1]]
limit = 100 #10

params = urllib.urlencode({'q': "+".join(terms), 'num':limit})
headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US    ; rv:1.9.0.9) Gecko/2009050519 Iceweasel/3.0.6 (Debian-3.0.6-1)'}
url = SEARCH_BASE_URL + "?" + params

conn = httplib.HTTPConnection(SEARCH_HOST)
conn.request("GET", url, {}, headers)
resp = conn.getresponse()
status = resp.status #200
papers = []
if status==200:
    html = resp.read()
    #file2 = open("scholar.htm","r")
    #html = file2.read()
    #file2.close()
    results = []
    html = html.decode('ascii', 'ignore')
    soup = BeautifulSoup(html)
    for record in soup('p'):
        potential_PDF_link = ""
        cluster_link = ""
        cluster_link_name = ""
        view_as_html_link = ""

        blah = record.find(name=re.compile("h3"))
        blah2 = record.find(name=re.compile("form"))
        #blah = True
        #blah2 = True
        if True:
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
                            potential_PDF_link = href
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
                    elif href.count("cluster") > 0: #All x versions
                        cluster_link = href
                        cluster_link_name = stuff.renderContents()
                    elif href.count("related") > 0: #related articles
                        related_link = href
                        related_link_name = stuff.renderContents()
                    elif stuff.renderContents() == "View as HTML":
                        view_as_html_link = href
                    elif stuff.renderContents() == "Cached":
                        pass
                        #TODO: add to record or object
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
                    publication = ""
                    pub_year = ""
                    if len(content_array) > 1:
                        if not len(content_array[1]) <= 6:
                            publication = content_array[1][:-6]
                        #last four digits should be a year
                        pub_year = content_array[1][-4:]
                        server = ""
                        if len(content_array) > 2:
                            server = content_array[2]
                            #print "server = ", server
                    #print "authors = ", author_data
                    #print "publisher = ", publication
                    #print "publication year = ", pub_year
                    
            #what now?
            diff_versions_link=cluster_link
            diff_versions_link_name=cluster_link_name
            print "what?"
            my_paper = Paper(title=paper_title, journal_href=journal_href, potential_PDF_link=potential_PDF_link, cites_link=cites_link, cites_link_name=cites_link_name, diff_versions_link=diff_versions_link, diff_versions_link_name=diff_versions_link_name, related_papers_link=related_link, view_as_html_link=view_as_html_link, authors=authors, publication=publication, pub_year=pub_year, server=server)
            papers.append(my_paper)

print yaml.dump(papers)
