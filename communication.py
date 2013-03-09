#!/usr/bin/python3.2
# -*- coding: iso-8859-15 -*-

import inspect # http://docs.python.org/3/library/inspect.html
import threading # http://docs.python.org/3/library/threading.html

from model import GameLogic
from interfaces import *
from pdu_codecs import ClientPduCodec, ServerPduCodec

class State: # default actions
    
    def name(self): 
        return self.__class__.__name__

    # add here methods with error-messages

#class CommClient():
#    entity = ClientPduCodec(self)
 

