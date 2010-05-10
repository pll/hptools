#!/usr/bin/python
"""
Test ilolib components
"""
import unittest

import urlparse
for scheme in 'ssh',:
    if not scheme in urlparse.uses_netloc:
        urlparse.uses_netloc += scheme,
    if not scheme in urlparse.uses_query:
        urlparse.uses_query += scheme,

import ilolib

testurl = "ssh://testuser:testpass@ilo16"
#testurl = "ssh://testuser:testpass@irish.lab.bos.redhat.com"

class TestIlo(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testIlo(self):
        i = ilolib.Ilo(url=testurl)

        print i._url
        print i._urlstring

        i.execute("show /map1")

        #url = urlparse.urlparse(testurl)

        #j = ilolib.Ilo(url=url)
        #print j._url
        #print j._urlstring

        #k = ilolib.Ilo("ilo16", "Administrator", "24^goldA")
        #print k._url
        #print k._urlstring

#import sys
#if sys.version_info[0] == 2 and sys.version_info[1] < 5:
import types

class TestParseResult(unittest.TestCase):

    def setUp(self):
        self.urlstrings = (
            "http://hostname", 
            "http://username@hostname",
            "http://username:password@hostname"
            )
            
    def testParseResult(self):
        for urlstring in self.urlstrings:

            a = urlparse.urlparse(urlstring)

            if type(a) == "<class 'urlparse.ParseResult'>":
                continue

            b = ilolib.ParseResult(a)

            print b.geturl()
            print b.hostname
            print b.username
            print b.password

if __name__ == "__main__":
    unittest.main()
