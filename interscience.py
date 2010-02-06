#!/usr/bin/python
#author: Bryan Bishop <kanzure@gmail.com>
#date: 2010-02-06
#usage: python interscience.py "http://www3.interscience.wiley.com/journal/123190541/abstract" blah.pdf
import optfunc
import os

def interscience2pdf(id, output_file):
    '''retrieves a PDF from an interscience.wiley.com link'''
    url = "http://download.interscience.wiley.com/cgi-bin/fulltext?ID=%s&PLACEBO=IE.pdf&mode=pdf" % (id)
    os.system("wget \"%s\" --output-document \"%s\"" % (url, output_file))

if __name__ == "__main__":
    optfunc.run(interscience2pdf)
