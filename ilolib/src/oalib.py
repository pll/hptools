"""
Manage communication via SSH with an HP BladeServer Open Administrator
"""
import logging

import ilourl

import ilolib
import pxssh
pxssh = pxssh.pxssh

class OpenAdministratorError(Exception): pass

class OpenAdministrator(ilolib.Ilo):

    _PROMPT = "ra-c7000-01-oa1> "

