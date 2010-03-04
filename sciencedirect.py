#!/usr/bin/python
#author: Bryan Bishop <kanzure@gmail.com>
#date: 2010-03-03
#purpose: given a link on the command line to sciencedirect.com, download the associated PDF and put it in "sciencedirect.pdf" or something
import os
import re
import optfunc
import pycurl
#from BeautifulSoup import BeautifulSoup
from lxml import etree
import lxml.html
from StringIO import StringIO
from string import join, split

user_agent = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.5) Gecko/20091123 Iceweasel/3.5.5 (like Firefox/3.5.5; Debian-3.5.5-1)"

def interscience(url):
    '''downloads the PDF from sciencedirect given a link to an article'''

    url = str(url)
    buffer = StringIO()

    curl = pycurl.Curl()
    curl.setopt(curl.URL, url)
    curl.setopt(curl.WRITEFUNCTION, buffer.write)
    curl.setopt(curl.VERBOSE, 0)
    curl.setopt(curl.USERAGENT, user_agent)
    curl.setopt(curl.TIMEOUT, 20)
    curl.perform()
    curl.close()

    buffer = buffer.getvalue().strip()
    html = lxml.html.parse(StringIO(buffer))
    image = html.findall("//img[@name='pdf']")[0]
    link = image.getparent()
    pdf_href = link.attrib["href"]

    #now let's get the article title
    title_div = html.findall("//div[@class='articleTitle']")[0]
    paper_title = title_div.text
    paper_title = paper_title.replace("\n", "")
    if paper_title[-1] == " ": paper_title = paper_title[:-1]
    re.sub('[^a-zA-Z0-9_\-.() ]+', '', paper_title)

    #now fetch the document for the user
    os.system("wget --user-agent=\"pyscholar/blah\" --output-document=\"%s.pdf\" \"%s\"" % (paper_title, pdf_href))
    print "\n\n"

if __name__ == "__main__":
    optfunc.run(interscience)
