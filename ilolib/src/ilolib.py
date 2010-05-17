"""
A library to help manage HP ILO Instances
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
import ilossh 
import ilourl


# ============================================================================
#
# Now back to our regularly scheduled library
#
# ============================================================================

sshpath = "/usr/bin/ssh"
# Assume that the command will include a new line and 
sshformat = "%s %s@%s %s\n%s"

class IloError(Exception):
    """
    A simple error object to allow us to distinguish between Ilo related errors.
    """
    pass


class Ilo(object):
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

    _PROMPT = "<.*>hpiLO-> "

    def __init__(self, url):
        """
        Create an Ilo instance.

        The Ilo object uses SSH to communicate with the remote Ilo service.

        ilo = Ilo(url="urlstring")
        ilo = Ilo("myhost", "username", "password")
        """

        if type(url) == types.StringType:
            url = urlparse.urlparse(url, "ssh")
            
        if type(url) == types.TupleType:
            self._url = ilourl.ParseResult(url)
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
            self._session = ilossh.ilossh()
            # catch bad host, or login failure
            try:
                self._session.login(self._url.hostname, 
                                    self._url.username, 
                                    self._url.password,
                                    login_timeout=30
                                    )
            except ilossh.EOF, e:
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

class IloResult(object):
    """
    An object that contains the parsed status of an ILO command
    """
    
    _command = None
    _status = None
    _statusTag = None
    _errorTag = None
    
    def __init__(self, buffer):
        
        lines = buffer.split("\r\n")

        self._command = lines[0]
        statusline = [line for line in lines if line.startswith('status=')][0]
        self._status = int(statusline[7:])
        statustagline = [line for line in lines if line.startswith('status_tag=')][0]
        self._statusTag = statustagline[11:]
        #errortaglines = [line for lines
        #self._errorTag = None
        
class IloNode(object):
    """
    An object to represent a node in a remote HP Ilo instance data tree
    """

    #__slots__ = (path, targets, properties, verbs, comment)
