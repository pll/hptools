"""
Enhance Python < 2.5 urlparse results
"""

# ============================================================================
#
# Enhance Python < 2.5 urlparse results
#
# ============================================================================
import re

import urlparse

class ParseResult(tuple):
    """
    Provide advanced urlparse ParseResult behavior for python < 2.5
    """

    netlocpattern = "(([^:]+)(:(\S+))?@)?(\S+)"
    netlocre = re.compile(netlocpattern)
    
    def __new__(cls, t=()):
        return tuple.__new__(cls, t)

    # Recompose the URL string from components
    def geturl(self):
        return urlparse.urlunparse(self)

    # get just the scheme component
    def _getScheme(self):
        return self[0]

    scheme = property(_getScheme)

    # get the network location component
    def _getNetloc(self):
        return self[1]

    netloc = property(_getNetloc)

    # get just the hostname part of the network location component
    def _getHostname(self):
        if self[1] == None:
            return None
        
        match = self.__class__.netlocre.match(self[1])
        return match.group(5)

    hostname = property(_getHostname)

    # get just the username part of the network location component
    def _getUsername(self):
        if self[1] == None:
            return None

        match = self.__class__.netlocre.match(self[1])
        return match.group(2)

    username = property(_getUsername)

    # get just the password part of the network location component
    def _getPassword(self):
        if self[1] == None:
            return None

        match = self.__class__.netlocre.match(self[1])
        return match.group(4)

    password = property(_getPassword)

    def _getPath(self):
        return self[2]

    path = property(_getPath)

    def _getParams(self):
        return self[3]

    params = property(_getParams)

    def _getQuery(self):
        return self[4]

    query = property(_getQuery)

    def _getFragment(self):
        return self[5]

    fragment = property(_getFragment)

