"""
This program begins with an empty Parse database and
simulates a Daeious event from start to finish.
"""


# Import Python stuff.
from __future__ import print_function # apparently, has to be on first line
from pprint import pprint
import itertools
import math
import os
import random
import sys
import time

# Import stuff that Parse might use.
import httplib, json, urllib

# Import ParsePy stuff. ParsePy makes using Parse in Python much easier.
from parse_rest.connection import ParseBatcher, register, SessionToken
from parse_rest.datatypes import ACL, Function, Object
from parse_rest.role import Role
from parse_rest.user import User

# Import Firebase stuff (https://github.com/mikexstudios/python-firebase)
from firebase import Firebase
import requests

# Import custom functions and classes I've written specifically for Daeious.
from helpers import batch_delete_from_Parse
from helpers import batch_delete_from_Parse_all_objects_of_class
from helpers import batch_upload_to_Parse
from helpers import create_QA_database_in_Firebase
from helpers import create_SAC_database_in_Firebase
from helpers import fetch_object_from_Parse_of_class
from helpers import register_with_Parse

register_with_Parse()

################################################################################
################################################################################
################################################################################
###                                                                          ###
"""                             PARSE CLASSES                                """
###                                                                          ###
################################################################################
################################################################################
################################################################################

# Create empty classes to match each class in Parse so they can be referenced.
    

 
 


################################################################################
################################################################################
################################################################################
###                                                                          ###
"""                                 GLOBALS                                  """
###                                                                          ###
################################################################################
################################################################################
################################################################################

# programmer-determined globals
EVENT_NUMBER = 0
MEN = 50
WOMEN = 50

# (must be set here so event-specific Parse classes can use it in their names)
EVENT_SERIAL = "{}{}".format("0"*(4 - len(str(EVENT_NUMBER))), EVENT_NUMBER)


# general Parse global classes
class Config(Object): pass
class Employee(Object): pass
class Event(Object): pass
class Ghost(Object): pass
class Interaction(Object): pass
class IPad(Object): pass
class Question(Object): pass
class Round(Object): pass
class Test_Class(Object): pass 

# event-specific Parse global classes
str_event_user_class_name = "zE" + EVENT_SERIAL + "_User"
str_r1_ix_class_name = "zE" + EVENT_SERIAL + "R1_Ix"
str_r2_ix_class_name = "zE" + EVENT_SERIAL + "R2_Ix"
str_r3_ix_class_name = "zE" + EVENT_SERIAL + "R3_Ix"
cls_EventUser = Object.factory(str_event_user_class_name)
cls_R1Ix = Object.factory(str_r1_ix_class_name)
cls_R2Ix = Object.factory(str_r2_ix_class_name)
cls_R3Ix = Object.factory(str_r3_ix_class_name)

# calculated globals
MAX_SEX = max(MEN,WOMEN)
STATIONS = MAX_SEX if MAX_SEX % 2 == 1 else MAX_SEX + 1
MALE_GHOSTS = STATIONS - MEN
FEMALE_GHOSTS = STATIONS - WOMEN
IPADS = 2 * STATIONS
EVENT_USERS = MEN + WOMEN + MALE_GHOSTS + FEMALE_GHOSTS

QUERY = cls_EventUser.Query.all()
count = cls_EventUser.Query.all().count()
LI_EVENT_USERS = list(
    cls_EventUser.Query.all().limit(1000).order_by("event_userNum"))
print(len(QUERY), count, len(LI_EVENT_USERS))

LI_STATION_NUMS = range(1, STATIONS + 1)
LI_M_IPAD_NUMS = range(1, STATIONS + 1)
LI_F_IPAD_NUMS = range(STATIONS + 1, 2*STATIONS + 1, 1)
LI_QUESTION_NUMS = range(1, STATIONS + 1)





################################################################################
################################################################################
################################################################################
###                                                                          ###
"""                                 CLASSES                                  """
###                                                                          ###
################################################################################
################################################################################
################################################################################


 


################################################################################
"""                                  _EVENT                                  """
################################################################################

class _Event(Object):

    EVENT_DATE = time.strftime("%Y.%m.%d")
    EVENT_TIME = random.choice(["19:00", "19:30", "20:00", "20:30", "21:00"])
    EVENT_LOCATION = random.choice(["Palo Alto", "San Francisco", "Los Angeles"])

    def __init__(self):
                
        # self.event_num = EVENT_NUMBER
        # self.event_serial = EVENT_SERIAL
        # self.event_date = _Event.EVENT_DATE
        # self.event_time = _Event.EVENT_TIME
        # self.event_location = _Event.EVENT_LOCATION
        # self.num_men = MEN
        # self.num_women = WOMEN
        # self.num_m_ghosts = MALE_GHOSTS
        # self.num_f_ghosts = FEMALE_GHOSTS
        # self.num_stations = STATIONS
        # self.num_ipads = STATIONS*2
        # self.num_r1_ix_pp = STATIONS/1.0
        # self.num_r2_ix_pp = STATIONS/4.0
        # self.num_r3_ix_pp = STATIONS/12.0

        # Create a corresponding Event object in Parse upon initialization.
        self.create_event_object_in_Parse()

        # Create event-user (zE_0000_User) objects in Parse upon initialization.
        self.li_eu = self.create_event_users_in_Parse()

        # Create a skeleton DB in Firebase
        self.create_QA_and_SAC_databases_in_Firebase()

        pass


    def create_event_object_in_Parse(self):
        # Create a corresponding Event object in Parse upon initialization.
        e = Event() # Remember, this is a *Parse* Event object, so it's ok!
        e.eventNum = EVENT_NUMBER
        e.eventPrefix = EVENT_SERIAL
        e.location = _Event.EVENT_LOCATION
        e.start = [_Event.EVENT_DATE, _Event.EVENT_TIME]
        e.startDate = _Event.EVENT_DATE
        e.startTime = _Event.EVENT_TIME
        e.numMen = MEN
        e.numWomen = WOMEN
        e.numUsers = MEN + WOMEN
        e.numMaleGhosts = MALE_GHOSTS
        e.numFemaleGhosts = FEMALE_GHOSTS
        e.numStations = STATIONS
        e.numIPads = 2*STATIONS
        e.num_r1_ix_pp = STATIONS/1.0
        e.num_r2_ix_pp = STATIONS/4.0
        e.num_r3_ix_pp = STATIONS/12.0
        e.save()
        pass


    def create_event_users_in_Parse(self):

        # For now, just grab first ones; later, check by array_eventsRegistered.

        """
        Create zE0000_User objects by "batch_save"-ing them to Parse using 
        ParsePy's ParseBatcher(). Event User objects are _User objects whose 
        array_eventsRegistered contains the eventNum of this current event.

        """

        eu_ClassName = "zE" + EVENT_SERIAL + "_User"
        eu_Class = Object.factory(eu_ClassName)


        # # Get the correct class name from the ep = Event Prefix (passed in).
        # eventUser_ClassName = ep + "_User"
        # eventUser_Class = Object.factory(eventUser_ClassName)

        # add some Users to this Event
        qset_all_users = User.Query.all().order_by("userNum")
        li_meu = list(qset_all_users.filter(sex = "M").limit(MEN))
        li_feu = list(qset_all_users.filter(sex = "F").limit(WOMEN))
        li_mgeu = list(qset_all_users.filter(sex = "MG").limit(MALE_GHOSTS))
        li_fgeu = list(qset_all_users.filter(sex = "FG").limit(FEMALE_GHOSTS))

        li_users_at_event = li_meu + li_feu + li_mgeu + li_fgeu

        count_eu = len(li_users_at_event)

        li_eu_obj_to_upload = []


        for index, obj_User in enumerate(li_users_at_event):
            new_EU_object = eu_Class(
                user_objectId = obj_User.objectId,
                event_userNum = index + 1,
                username = obj_User.username,
                first = obj_User.username.split(" ")[0],
                last = obj_User.username.split(" ")[-1],
                sex = obj_User.sex
            )
            li_eu_obj_to_upload.append(new_EU_object)


        # Batch upload in chunks no larger than 50, 
        # and sleep to avoid timeouts
        batch_upload_to_Parse(eu_ClassName, li_eu_obj_to_upload)    

        return li_eu_obj_to_upload


    def create_QA_and_SAC_databases_in_Firebase(self):
        pass

    def simulate(self):
        # simulates an entire event (all 3 rounds, plus pregame and postgame)
        r0 = Round_0()
        r1 = Round_1()
        r2 = Round_2()
        r3 = Round_3()
        r4 = Round_4()

        print("\nRound objects created.")

        for r in [r0, r1, r2, r3, r4]:
            print("\nCurrent Round:", r.round_num)
            r.prepare()
            r.simulate()
            r.analyze()
       
        pass



################################################################################
"""                                  _ROUND                                  """
################################################################################

class _Round(Object):

    CURRENT_ROUND = -1

    print (len(LI_EVENT_USERS))

    LI_EVENT_USERS = []

    print (len(LI_EVENT_USERS))

    def __init__(self):

        # Increment the current round.
        _Round.CURRENT_ROUND += 1

        # Initialize the round_num variable (Round_3 will set it to 3, for ex.)
        self.round_num = None

        # Initialize the sec_per_ix variable (differs by round)
        self.sec_per_ix = None

        # Initialize the round_time variable (equals #stations * sec_per_ix)
        self.sec_in_round = None

        # Fill the class list of event users.
        _Round.LI_EVENT_USERS = list(cls_EventUser.Query.all().order_by("euNum"))

        # Refresh the global list of event users
        LI_EVENT_USERS = _Round.LI_EVENT_USERS

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


################################################################################
"""                               _INTERACTION                               """
################################################################################

################################################################################
"""                                  _USER                                   """
################################################################################

################################################################################
"""                                _QUESTION                                 """
################################################################################




################################################################################
################################################################################
################################################################################
###                                                                          ###
"""                                  MAIN                                    """
###                                                                          ###
################################################################################
################################################################################
################################################################################

def main():
    """
    1. Register with Parse.
    2. Delete all existing desired objects from Parse.
    3. Simulate event.
    4. Run tests on results.

    """

    # 1. Register with Parse.
    register_with_Parse() 


    ## 2. Delete existing event-specific objects from Parse 
    ## to maintain sanity when testing.
    ## (The for: loop should work too, but if I want to save time when testing,
    ## I can comment out individual lines, so that's how I've kept them)
    # for cls in ["Event", "Round", "zE_0000_User", "zE_0000_R1", "zE_0000_R2", 
    # "zE_0000_R3"]:
    #     batch_delete_from_Parse_all_objects_of_class(cls)

    batch_delete_from_Parse_all_objects_of_class("Event")
    batch_delete_from_Parse_all_objects_of_class("Round")
    batch_delete_from_Parse_all_objects_of_class(str_event_user_class_name)
    batch_delete_from_Parse_all_objects_of_class(str_r1_ix_class_name)
    batch_delete_from_Parse_all_objects_of_class(str_r2_ix_class_name)
    batch_delete_from_Parse_all_objects_of_class(str_r3_ix_class_name)


    # 3. Simulate event

    # 3a. Create an _Event object.
    e = _Event()

    # 3b. Simulate the entire event.
    e.simulate()



    # 4. Run tests on the results.

    pass


if __name__ == '__main__':
    status = main()
    print("\n---\n\ndaeious.py has finished running.\n")
    sys.exit(status)































