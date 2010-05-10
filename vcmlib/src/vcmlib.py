"""
A library to help manage HP Virtual Connection Manager
"""

import logging

import urlparse
# Add ssh to the allowable schemes if it's not there.
for scheme in ('ssh',):
    if not scheme in urlparse.uses_netloc:
        urlparse.uses_netloc += [scheme]
    if not scheme in urlparse.uses_query:
        urlparse.uses_query += [scheme]

import types
import vcmurl, vcmssh

class VirtualConnectionManagerError(Exception): pass

class VirtualConnectionManager(object):
    """
    This object allows command execution on a remote HP Virtual Connection
    Manager instance.

    vcm = VirtualConnectionManager(url="urlstring")
    vcm = VirtualConnectionManager(hostname="myhost", 
                                   username="username", password="password")
    response = vcm.execute(commandstring)
    response = vcm.execute("command", "argument0", "argument1"...)
    value = vcm.show(path, attribute)
    vcm.set(path, attribute, value)

    The communications protocol must be SSH
    """

    _PROMPT = "\n->"
    
    def __init__(self, url):

        """
        Create A VirtualConnectionManager instance.

        The VCM object uses SSH to communicate with the remote VCM service.

        vcm = VirtualConnectionManager(url="urlstring")
        vcm = VirtualConnectionManager("myhost", "username", "password")
        """

        if type(url) == types.StringType:
            url = urlparse.urlparse(url, "ssh")
            
        if type(url) == types.TupleType:
            self._url = vcmurl.ParseResult(url)
            self._urlstring = "%s://%s" % (url[0], url[1])

        elif isinstance(url, urlparse.ParseResult):
            self._url = url
            self._urlstring = url.geturl()

        self._session = None

    def execute(self, *cmd):
        """
        Execute a single command on a remote Ilo instance.
        Return the resulting string
        """

        self.connect()
        self._session.sendline(' '.join(cmd))
        self._session.prompt()
        response = self._session.before
        #result = IloResult(self._session.before)
        #node = IloNode(self._session.before)
        self.disconnect()
        # return (result, node)
        return response

    def connect(self):
        if self._session == None:
            self._session = vcmssh.vcmssh()
            # catch bad host, or login failure
            try:
                self._session.login(self._url.hostname, 
                                    self._url.username, 
                                    self._url.password,
                                    original_prompt=self._PROMPT,
                                    auto_prompt_reset=False,
                                    login_timeout=30
                                    )
            except vcmssh.EOF, e:
                raise IloError("cannot log into host '%s'" % self._url.hostname)

            self._session.PROMPT = self._PROMPT

    def disconnect(self):
        if self._session != None:
            self._session.logout()
            self._session = None

    def show(self, path, prop=None):
        pass

    def set(self, path, prop, value):
        pass
