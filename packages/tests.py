#!/usr/bin/python
import unittest
import classes

class TestScienceDirect(unittest.TestCase):
    def test_detectWeb(self):
        sci = classes.ScienceDirect()
        #some_file = open("../tests/science-direct.html","r") #-search-results.html","r")
        some_file = open("../tests/science-direct-search-results.html","r")
        contents = some_file.read()
        some_file.close()
        url = "http://www.sciencedirect.com/science?_ob=ArticleListURL&_method=list&_ArticleListID=966440345&_sort=r&view=c&_acct=C000059713&_version=1&_urlVersion=0&_userid=108429&md5=68c788df065c832e7749a7ae42d0261e"
        doc = contents
        self.assertTrue(sci.detectWeb(doc, url)=="multiple")

        some_file = open("../tests/science-direct.html", "r")
        contents = some_file.read()
        some_file.close()
        url = "http://www.sciencedirect.com/science?_ob=ArticleURL&_udi=B6TCM-4P0N8VD-1&_user=108429&_coverDate=09%2F01%2F2007&_alid=966440345&_rdoc=1&_fmt=high&_orig=search&_cdi=5174&_sort=r&_docanchor=&view=c&_ct=4415&_acct=C000059713&_version=1&_urlVersion=0&_userid=108429&md5=8cb00d3406086acb499b7c204ba76715"
        doc = contents
        self.assertTrue(sci.detectWeb(doc, url)== "journalArticle")
        return
    def test_doWeb(self):
        sci = classes.ScienceDirect()
        some_file = open("../tests/science-direct-search-results.html", "r")
        contents = some_file.read()
        some_file.close()
        url = "http://www.sciencedirect.com/science?_ob=ArticleListURL&_method=list&_ArticleListID=966440345&_sort=r&view=c&_acct=C000059713&_version=1&_urlVersion=0&_userid=108429&md5=68c788df065c832e7749a7ae42d0261e"
        doc = contents
        print sci.doWeb(doc, url)
        return

if __name__ == '__main__':
    unittest.main()
