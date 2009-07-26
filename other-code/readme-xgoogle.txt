This is a Google library called 'xgoogle'. Current version is 1.1.

It's written by Peteris Krumins (peter@catonmat.net).
His blog is at http://www.catonmat.net  --  good coders code, great reuse.

--------------------------------------------------------------------------

At the moment it contains:
 * Google Search module xgoogle/search.py.
   http://www.catonmat.net/blog/python-library-for-google-search/

 * Google Sponsored Links Search module xgoogle/sponsoredlinks.py
   http://www.catonmat.net/blog/python-library-for-google-sponsored-links-search/

--------------------------------------------------------------------------

Here is an example usage of Google Search module:

    >>> from xgoogle.search import GoogleSearch
    >>> gs = GoogleSearch("catonmat")
    >>> gs.results_per_page = 25
    >>> results = gs.get_results()
    >>> for res in results:
    ...   print res.title.encode('utf8')
    ... 

    output:

    good coders code, great reuse
    MIT's Introduction to Algorithms, Lectures 1 and 2: Analysis of ...
    catonmat - Google Code
    ...

The GoogleSearch object has several public methods and properties:

    method get_results() - gets a page of results, returning a list of SearchResult objects.
    property num_results - returns number of search results found.
    property results_per_page - sets/gets the number of results to get per page.
    property page - sets/gets the search page.

A SearchResult object has three attributes -- "title", "desc", and "url". They are Unicode strings, so do a proper encoding before outputting them.

--------------------------------------------------------------------------

Here is an example usage of Google Sponsored Links Search module:

    >>> from xgoogle.sponsoredlinks import SponsoredLinks, SLError
    >>> sl = SponsoredLinks("video software")
    >>> sl.results_per_page = 100
    >>> results = sl.get_results()
    >>> for result in results:
    ...   print result.title.encode('utf8')
    ...

    output:

    Photoshop Video Software
    Video Poker Software
    DVD/Video Rental Software
    ...

The SponsoredLinks object has several public methods and properties:

    method get_results() - gets a page of results, returning a list of SearchResult objects.
    property num_results - returns number of search results found.
    property results_per_page - sets/gets the number of results to get per page.

A SponsoredLink object has four attributes -- "title", "desc", "url", and "display_url".

--------------------------------------------------------------------------

Version history:

v1.0:  * initial release, xgoogle library contains just the Google Search.
v1.1:  * added Google Sponsored Links Search.
       * fixed a bug in browser.py that might have thrown an unexpected exception.

--------------------------------------------------------------------------

That's it. Have fun! :)


Sincerely,
Peteris Krumins
http://www.catonmat.net

