"""
A library to help communicate via SSH with HP BladeSystem Open Administrator
"""
import logging

import types

import urlparse
for scheme in ('ssh', ):
    if not scheme in urlparse.uses_netloc:
        urlparse.uses_netloc += [scheme]
    if not scheme in urlparse.uses_query:
        urlparse.uses_query += [scheme]

import oaurl

import oassh

class OpenAdministrator(object):
    """
    An object to communicate with an HP BladeSystem Open Administrator instance
    """

    _PROMPT = "\n\S+> "

    def __init__(self, url):

        if type(url) == types.StringType:
            self._urlstring = url
            self._url = urlparse.urlparse(url)
            
        elif type(url) == types.TupleType:
            self._url = oaurl.ParseResult(url)
            self.urlstring = self._url.geturl()
        else:
            self._url = url
            self._urlstring = url.geturl()

        logging.debug("url = %s" % str(self._url))

        self._session = None

    def execute(self, *cmd):
        
        logger = logging.getLogger(self.__class__.__name__ + ".execute")

        self._session = oassh.oassh()
        logger.debug("logging in")
        self._session.login(self._url.hostname, 
                            self._url.username, self._url.password,
                            original_prompt = self._PROMPT,
                            auto_prompt_reset = False)

        self._session.PROMPT=self._PROMPT
        logger.debug("Sending command")
        self._session.sendline(' '.join(cmd))
        logger.debug("Waiting for prompt")
        self._session.prompt()
        logger.debug("returning bracketed text")
        return self._session.before


