
import logging

import types

import urlparse

import saurl
import sassh

class Storage(object):
    """
    This object allows command execution on a remote HP Ilo 2 instance.

    ilo = Ilo(url="urlstring")
    ilo = Ilo(hostname="myhost", username="username", password="password")
    response = ilo.execute(commandstring)
    response = ilo.execute("command", "argument0", "argument1"...)
    value = ilo.show(path, attribute)
    ilo.set(path, attribute, value)

    The communications protocol must be SSH

    """

    _PROMPT = "\n# "

    def __init__(self, url):
        """
        Create a Storage instance.

        The Storage object uses SSH to communicate with the remote Storage Manager service.

        storage = Storage(url="urlstring")
        storage = Storage("myhost", "username", "password")
        """

        if type(url) == types.StringType:
            url = urlparse.urlparse(url, "ssh")
            
        if type(url) == types.TupleType:
            self._url = saurl.ParseResult(url)
            self._urlstring = "%s://%s" % (url[0], url[1])

        elif isinstance(url, urlparse.ParseResult):
            self._url = url
            self._urlstring = url.geturl()

        self._session = None

    # def __del__(self):
    #     """Remove any hanging connections on destruction of the Ilo object"""
    #     pass

    def execute(self, *cmd):
        """
        Execute a single command on a remote Ilo instance.
        Return the resulting string
        """

        cmdstring = ' '.join(cmd)
        self.connect()
        self._session.sendline(cmdstring)
        # add this if you want to suppress the command input echo
        #self._session.expect(cmdstring)
        self._session.prompt()
        response = self._session.before
        #result = IloResult(self._session.before)
        #node = IloNode(self._session.before)
        self.disconnect()
        # return (result, node)
        return response

    def connect(self):
        if self._session == None:
            self._session = sassh.sassh()
            # catch bad host, or login failure
            try:
                self._session.login(self._url.hostname, 
                                    self._url.username, 
                                    self._url.password,
                                    original_prompt = "\n# ",
                                    auto_prompt_reset=False
                                    )
            except sassh.EOF, e:
                raise IloError("cannot log into host '%s'" % self._url.hostname)

            self._session.PROMPT = self._PROMPT
            self._session.sendline("set cli-parameters pager off")
            self._session.prompt()

    def disconnect(self):
        if self._session != None:
            self._session.logout()
            self._session = None

    def show(self, path, prop=None):
        pass

    def set(self, path, prop, value):
        pass

