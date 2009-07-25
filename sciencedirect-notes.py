#!/usr/bin/python
from gsearch import *
import re

#related articles href =
#gs("/html/body/div[1]/div/div[@id='sdBody']/div/div[@id='rightCol']/div/div[@id='searchResults']/div[@id='bodyMainResults']/table[1]/tr/td[2]/div/a[2]")[0].values()[0]

#sciencedirect results page
#paper_title and paper_link
#paper_temp = gs("/html/body/div[1]/div/div[@id='sdBody']/div/div[@id='rightCol']/div/div[@id='searchResults']/div[@id='bodyMainResults']/table/tr/td[2]/a")
#for each in paper_temp:
#    paper_title = ""
#    paper_link = ""
#    for piece in paper_temp.itertext():
#        paper_title = paper_title + piece
#    paper_link = paper_temp.items()[0][1]


results = gs("/html/body/div[1]/div/div[@id='sdBody']/div/div[@id='rightCol']/div/div[@id='searchResults']/div[@id='bodyMainResults']/table")
number_of_results = len(results)
for result in results:
    paper_title = ""
    paper_link = ""
    related_articles_href = result.xpath("tr/td[2]/div/a[contains(.,'Related')]")[0].values()[0]
    title_temp = result.xpath("tr/td[2]/a[1]")
    for one in title_temp:
        for piece in one.itertext():
            paper_title = paper_title + piece
        paper_link = one.items()[0][1]
    #now for the PDF link
    pdf_link = ""
    pdf_results = result.xpath("tr/td[2]/div/a[contains(.,'PDF')]")
    for piece in pdf_results:
        query = re.compile("PDF")
        text = ""
        for piece2 in piece.itertext():
            text = text + piece2
        if len(query.findall(text))>0:
            pdf_link = piece.values()[0]

    #paper_title
    #paper_link
    #related_articles_href
    #pdf_link
    print "paper_title = ", paper_title.encode("utf-8","backslashreplace")
    print "paper_link = ", paper_link.decode("iso-8859-15")
    print "related_link = ", related_articles_href
    print "pdf = ", pdf_link

