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
###																			 ###
"""                             PARSE CLASSES                                """
###																			 ###
################################################################################
################################################################################
################################################################################

# Create empty classes to match each class in Parse so they can be referenced.
    

 
 


################################################################################
################################################################################
################################################################################
###																			 ###
"""                                 GLOBALS                                  """
###																			 ###
################################################################################
################################################################################
################################################################################

EVENT_NUMBER = 0
MEN = 50
WOMEN = 50

EVENT_SERIAL = "{}{}".format("0"*(4 - len(str(EVENT_NUMBER))), EVENT_NUMBER)


 # general Parse classes
class Config(Object): pass
class Employee(Object): pass
class Event(Object): pass
class Ghost(Object): pass
class Interaction(Object): pass
class IPad(Object): pass
class Question(Object): pass
class Round(Object): pass
class Test_Class(Object): pass 

# event-specific Parse classes
str_event_user_class_name = "zE" + EVENT_SERIAL + "_User"
str_r1_ix_class_name = "zE" + EVENT_SERIAL + "R1_Ix"
str_r2_ix_class_name = "zE" + EVENT_SERIAL + "R2_Ix"
str_r3_ix_class_name = "zE" + EVENT_SERIAL + "R3_Ix"
cls_EventUser = Object.factory(str_event_user_class_name)
cls_R1Ix = Object.factory(str_r1_ix_class_name)
cls_R2Ix = Object.factory(str_r2_ix_class_name)
cls_R3Ix = Object.factory(str_r3_ix_class_name)


MAX_SEX = max(MEN,WOMEN)
STATIONS = MAX_SEX if MAX_SEX % 2 == 1 else MAX_SEX + 1
MALE_GHOSTS = STATIONS - MEN
FEMALE_GHOSTS = STATIONS - WOMEN
IPADS = 2 * STATIONS

LI_EVENT_USERS = list(cls_EventUser.Query.all().order_by("event_userNum"))

LI_STATION_NUMS = list(x+1 for x in range(STATIONS))
LI_M_IPAD_NUMS = list(x+1 for x in range(0, STATIONS, 1))
LI_F_IPAD_NUMS = list(x+1 for x in range(STATIONS, 2*STATIONS, 1))
LI_QUESTION_NUMS = list(x+1 for x in range(STATIONS))





################################################################################
################################################################################
################################################################################
###																			 ###
"""                                 CLASSES                                  """
###																			 ###
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

        for r in [r0, r1, r2, r3, r4]:
            r.prepare()
            r.simulate()
            r.analyze()
       
        pass





################################################################################
"""                                  _ROUND                                  """
################################################################################

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
###															 				 ###
"""                                  MAIN                                    """
###															   				 ###
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
    print("\n\ndaeious.py has finished running.\n")
    sys.exit(status)































