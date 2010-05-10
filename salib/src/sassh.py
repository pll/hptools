import time

import pxssh

TIMEOUT = pxssh.TIMEOUT
EOF = pxssh.EOF


class sassh(pxssh.pxssh):

    def sendline(self, s='', linesep="\r\n"):

        """This is like send(), but it adds a line feed (os.linesep). This
        returns the number of bytes written. """

        n = self.send(s)
        n = n + self.send (linesep)
        return n

    def synch_original_prompt (self):

        """This attempts to find the prompt. Basically, press enter and record
        the response; press enter again and record the response; if the two
        responses are similar then assume we are at the original prompt. """

        # All of these timing pace values are magic.
        # I came up with these based on what seemed reliable for
        # connecting to a heavily loaded machine I have.
        # If latency is worse than these values then this will fail.

        try:
            self.read_nonblocking(size=10000,timeout=1) # GAS: Clear out the cache before getting the prompt
        except TIMEOUT:
            pass
        time.sleep(0.1)
        self.sendline()
        time.sleep(0.5)
        x = self.read_nonblocking(size=1000,timeout=1)
        time.sleep(0.1)
        self.sendline()
        time.sleep(0.5)
        a = self.read_nonblocking(size=1000,timeout=1)
        time.sleep(0.1)
        self.sendline()
        time.sleep(0.5)
        b = self.read_nonblocking(size=1000,timeout=1)
        ld = self.levenshtein_distance(a,b)
        len_a = len(a)
        if len_a == 0:
            return False
        if float(ld)/len_a < 0.4:
            return True
        return False
