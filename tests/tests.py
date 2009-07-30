#!/usr/bin/python
#tests.py - test codebase

import unittest
import pyscholar

class TestResolver(unittest.TestCase):
    def test_pyscholar_resolver(self):
        '''test pyscholar.resolve()'''
        #pyscholar.resolve(some_search_result) should go grab the pdf and metadata for a result object
        pass

class TestGoogleScholar(unittest.TestCase):
    def test_google_search(self):
        '''test pyscholar.packages.GoogleScholar'''
        google_scholar = pyscholar.packages.GoogleScholar(lang=en)
        results = google_scholar.query("PDMS", count=100)

        #there must be at least one result for that query
        self.assertTrue(len(results)>0)
        #in fact, we might as well demand there's 100 results
        self.assertTrue(len(results)==100)

        #not sure what else to test

        return
    def test_google_search_proxy(self):
        #TODO: test pyscholar.packages.GoogleScholar() with ezproxy proxy
        pass
 
class TestScienceDirect(unittest.TestCase):
    def test_sciencedirect_search(self):
        num_results = 50
        
        sciencedirect = pyscholar.packages.ScienceDirect()
        results = sciencedirect.query("PDMS", count=num_results)

        #there must be at least one result for that query
        self.assertTrue(len(results)>0)
        #in fact, we might as well demand there's num_results results
        self.assertTrue(len(results)==num_results)
        
        #test values
        for result in results:
            real_result = pyscholar.resolve(result)
            #check that the values in 'result' match those in 'real_result' (the article page scrape)
        return
    def test_sciencedirect_article(self):
        sciencedirect = pyscholar.packages.ScienceDirect()
        article = sciencedirect.fetch("some article name here")
        #do what now?
        pass

if __name__ == '__main__':
    unittest.main()
