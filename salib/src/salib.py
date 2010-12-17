
import logging

import types

import urlparse

import saurl
import sassh

class Storage(object):
    """
    This object allows command execution on a remote HP MSA instance.

    msa = Msa(url="urlstring")
    msa = Msa(hostname="myhost", username="username", password="password")
    response = msa.execute(commandstring)
    response = msa.execute("command", "argument0", "argument1"...)
    value = msa.show(path, attribute)
    msa.set(path, attribute, value)

    The communications protocol must be SSH

    """

    _PROMPT = "\r\n# (\r)?"

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
    #     """Remove any hanging connections on destruction of the Msa object"""
    #     pass

    def execute(self, *cmd):
        """
        Execute a single command on a remote Msa instance.
        Return the resulting string
        """
        logger = logging.getLogger(self.__class__.__name__ + ".execute")

        cmdstring = ' '.join(cmd)
        logger.debug(" Command string = %s" % cmdstring)

        self.connect()
        logger.debug("Connected: Sending command string")
        self._session.sendline(cmdstring)

        # add this if you want to suppress the command input echo
        #self._session.expect(cmdstring)
        logger.debug("Waiting for prompt after command")
        self._session.prompt(timeout=30)
        response = self._session.before
        logger.debug("Response = '%s'" % response)
        logger.debug("session buffer = %s" % self._session.buffer)
            

        #result = MsaResult(self._session.before)
        #node = MsaNode(self._session.before)
        logger.debug("Disconnecting")
        self.disconnect()
        # return (result, node)
        return response

    def connect(self):
        logger = logging.getLogger(self.__class__.__name__ + ".connect")
        if self._session == None:
            self._session = sassh.sassh()
            # catch bad host, or login failure
            try:
                self._session.login(self._url.hostname, 
                                    self._url.username, 
                                    self._url.password,
                                    original_prompt = "\n# ",
                                    auto_prompt_reset=False,
                                    login_timeout=30
                                    )
                logger.debug("Logged in")
                logger.debug("After = '%s'" % self._session.after)
            except sassh.EOF, e:
                logger.debug("Login failed: %s" % e.message)
                raise MsaError("cannot log into host '%s'" % self._url.hostname)

            logger.debug("Setting prompt to '%s'" % self._PROMPT)
            self._session.PROMPT = self._PROMPT
            logger.debug("Setting pager off")
            self._session.sendline("set cli-parameters pager off")
            logger.debug("Waiting for first prompt after silencing the pager")
            self._session.prompt(timeout=30)

            logger.debug("session info = %s" % self._session.before)

    def disconnect(self):
        if self._session != None:
            self._session.logout()
            self._session = None

    def show(self, path, prop=None):
        pass

    def set(self, path, prop, value):
        pass

