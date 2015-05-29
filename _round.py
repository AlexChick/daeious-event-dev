"""
The Round class has methods for simulating and analyzing a round.

Also included are 5 subclasses: Round_1, Round_2, Round_3, Round_4, Round_5.
"""

###############################################################################

# Import Python stuff
from __future__ import print_function
from pprint import pprint
import itertools
import math
import os
import random
import sys
import time

# Import Parse stuff
import httplib, json, urllib

# Import ParsePy stuff
from parse_rest.connection import ParseBatcher, register, SessionToken
from parse_rest.datatypes import ACL, Function, Object
from parse_rest.role import Role
from parse_rest.user import User

# Import Firebase stuff (https://github.com/mikexstudios/python-firebase)
from firebase import Firebase
import requests

# Import custom functions and classes I've written specifically for Daeious.
from _interaction import _Interaction
from helpers import register_with_Parse
from helpers import batch_delete_from_Parse_all_objects_of_class


###############################################################################

class Round(Object): pass # needed for Parse Round class interactivity

class _Round(Object):

    CURRENT_ROUND = -1

    LI_EVENT_USERS = []

    def __init__(self):

        # Increment the current round.
        _Round.CURRENT_ROUND += 1

        # Initialize the round_num variable (Round_3 will set it to 3, for ex.)
        self.round_num = None

        # Initialize the sec_per_ix variable (differs by round)
        self.sec_per_ix = None

        # Initialize the round_time variable (equals #stations * sec_per_ix)
        self.sec_in_round = None

        # fill in the list of event users
        class zE0000_User(Object): pass
        _Round.LI_EVENT_USERS = list(zE0000_User.Query.all().order_by("euNum"))

        pass

    def create_round_object_in_Parse(self):
        # Will be called inside the initiator of Round_0, Round_1, etc.
        self.r = Round()
        self.r.roundNum = self.round_num
        self.r.secPerIx = self.sec_per_ix
        self.r.secInRound = self.sec_in_round
        self.r.save()
        pass

    def create_ix_objects(self):
        # queries Parse for all event users, 
        pass

    def prepare(self):
        self.create_ix_objects()
        pass

    def simulate(self):
        pass

    def analyze(self):
        pass


###############################################################################
"""                               Round 0                                   """
###############################################################################
        

class Round_0(_Round):
    """
    --> Pregame stuff. Assume sufficient (>100) Users exist in Parse.

    prepare: 
        - assign_pregame_sel_and_des_ranks() to all event-users
        - 
    simulate:
        - (Nothing to simulate)
    analyze:
        - (Nothing to analyze)
    ***
    assign_pregame_sel_and_des_ranks:
        -
    """

    def __init__(self):
        _Round.__init__(self)
        self.round_num = 0
        self.create_round_object_in_Parse()
        pass

    def assign_pregame_sel_and_des_ranks(self):
        pass

    def prepare(self):
        pass

    def simulate(self): 
        # nothing to do here
        pass

    def analyze(self):
        pass

    pass

###############################################################################
"""                               Round 1                                   """
###############################################################################

class Round_1(_Round):
    """
    --> All men and all women have 1 interaction with each other,
    moving to their right by 1 iPad / station for each new interaction.

    sec_per_ix: 
    - Given 50m/50w/1mg/1fg,
        sec_per_ix = 15 --> Round 1 is 51 * 15 = 765s = 12.75min = 12m45s.
        sec_per_ix = 20 --> Round 1 is 51 * 20 = 1020 = 17.00min = 17m00s.
    - (Should Round_1 be a constant number of minutes, so that interactions
        are longer when there are fewer people? Or should the sec_per_ix
        be a constant for each round? I'll have to play around with that.
        Right now, I'm leaning towards keeping sec_per_ix constant.)

    prepare: 
        - 
    simulate:
        - 
    analyze:
        - 
    """

    def __init__(self):
        _Round.__init__(self)
        self.round_num = 1
        self.sec_per_ix = 20
        self.create_round_object_in_Parse()
        pass

    def prepare(self):
        # make and upload to Parse all MEN * WOMEN interaction objects
        pass

    def simulate(self):
        pass

    def analyze(self):
        pass

    pass

###############################################################################
"""                               Round 2                                   """
###############################################################################

class Round_2(_Round):

    def __init__(self):
        _Round.__init__(self)
        self.round_num = 2
        self.sec_per_ix = 40
        self.create_round_object_in_Parse()
        pass

    def prepare(self):
        pass

    def simulate(self):
        pass

    def analyze(self):
        pass

    pass

###############################################################################
"""                               Round 3                                   """
###############################################################################

class Round_3(_Round):

    def __init__(self):
        _Round.__init__(self)
        self.round_num = 3
        self.sec_per_ix = 60
        self.create_round_object_in_Parse()
        pass

    def prepare(self):
        pass

    def simulate(self):
        pass

    def analyze(self):
        pass

    pass

###############################################################################
"""                               Round 4                                   """
###############################################################################

class Round_4(_Round):
    """
    Postgame stuff.
    """

    def __init__(self):
        _Round.__init__(self)
        self.round_num = 4
        self.create_round_object_in_Parse()
        pass

    def prepare(self):
        pass

    def simulate(self):
        pass

    def analyze(self):
        pass

    pass



###############################################################################
"""                                  MAIN                                   """
###############################################################################

def main():

    register_with_Parse()

    batch_delete_from_Parse_all_objects_of_class("Round")

    r0 = Round_0()
    r1 = Round_1()
    r2 = Round_2()
    r3 = Round_3()
    r4 = Round_4()

    print ("1:", r0.round_num)
    print ("2:", _Round.CURRENT_ROUND)
    print ("3:", r1.round_num)

if __name__ == '__main__':
    status = main()
    sys.exit(status)













