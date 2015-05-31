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
from helpers import mk_serial
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

# # programmer-determined globals
# global EVENT_NUMBER
# global MEN
# global WOMEN
# global START_AT_ROUND
# global SEC_PER_R1_IX
# global SEC_PER_R2_IX
# global SEC_PER_R3_IX

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
global str_event_user_class_name
global str_r1_ix_class_name
global str_r2_ix_class_name
global str_r3_ix_class_name
global cls_EventUser
global cls_R1Ix
global cls_R2Ix
global cls_R3Ix




# # calculated (yet static) globals
# MAX_SEX = max(MEN,WOMEN)
# STATIONS = MAX_SEX if MAX_SEX % 2 == 1 else MAX_SEX + 1
# MALE_GHOSTS = STATIONS - MEN
# FEMALE_GHOSTS = STATIONS - WOMEN
# IPADS = 2 * STATIONS
# EVENT_USERS = MEN + WOMEN + MALE_GHOSTS + FEMALE_GHOSTS
# NUM_R1_IX_PP = int(round(STATIONS/1.0, 0))
# NUM_R2_IX_PP = int(round(STATIONS/4.0, 0))
# NUM_R3_IX_PP = int(round(STATIONS/10.0, 0))
# NUM_EV_IX_PP = NUM_R1_IX_PP + NUM_R2_IX_PP + NUM_R3_IX_PP
# SEC_IN_R1 = NUM_R1_IX_PP * SEC_PER_R1_IX
# SEC_IN_R2 = NUM_R2_IX_PP * SEC_PER_R2_IX
# SEC_IN_R3 = NUM_R3_IX_PP * SEC_PER_R3_IX
# SEC_IN_EVENT = SEC_IN_R1 + SEC_IN_R2 + SEC_IN_R3

# LI_STATION_NUMS = range(1, STATIONS + 1)
# LI_SUBROUND_NUMS = range(1, STATIONS + 1)
# LI_M_IPAD_NUMS = range(1, STATIONS + 1)
# LI_F_IPAD_NUMS = range(STATIONS + 1, 2*STATIONS + 1, 1)
# LI_Q_NUMS = range(1, STATIONS + 1)
LI_R1_IX = []
LI_R2_IX = []
LI_R3_IX = []

# LI_M_EV_USERS = cls_EventUser.Query.all().filter(sex = "M").order_by("euNum")
# LI_F_EV_USERS = cls_EventUser.Query.all().filter(sex = "F").order_by("euNum")
# LI_M_IPAD_OBJS = IPad.Query.all().limit(STATIONS).order_by("iPadNum")
# LI_F_IPAD_OBJS = IPad.Query.all().skip(STATIONS).limit(STATIONS).order_by("iPadNum")
# LI_Q_OBJS = Question.Query.all().limit(1000).order_by("qNum")



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

    def __init__(self, EVENT_NUMBER = 0,
                       MEN = 20,
                       WOMEN = 20,
                       START_AT_ROUND = 0,
                       SEC_PER_R1_IX = 20,
                       SEC_PER_R2_IX = 40,
                       SEC_PER_R3_IX = 60
        ):

        # You CAN'T SET GLOBALS from within __init__ 
        # But you CAN assign to self.whatever

        # Set the Parse-specific global classes
        self.set_Parse_specific_global_classes(EVENT_NUMBER)

        # Set instance variables
        self.event_number = EVENT_NUMBER
        self.event_serial = mk_serial(EVENT_NUMBER)
        self.event_date = time.strftime("%Y.%m.%d")
        self.event_time = random.choice(["19:00", "19:30", "20:00", "20:30"])
        self.event_location = random.choice(["Heaven", "California"])

        self.num_m_eu_p = MEN
        self.num_f_eu_p = WOMEN
        self.num_all_eu_p = MEN + WOMEN

        self.max_sex = max(MEN,WOMEN)
        self.num_stations = self.max_sex if self.max_sex%2==1 else self.max_sex+1
        self.num_ipads = self.num_stations * 2

        self.num_m_eu_g = self.num_stations - MEN
        self.num_f_eu_g = self.num_stations - WOMEN
        self.num_all_eu_g = self.num_m_eu_g + self.num_f_eu_g 

        self.num_all_eu = self.num_all_eu_p + self.num_all_eu_g

        self.num_r1_ix_pp = int(round(self.num_stations/1.0, 0))
        self.num_r2_ix_pp = int(round(self.num_stations/4.0, 0))
        self.num_r3_ix_pp = int(round(self.num_stations/12.0, 0))
        self.num_event_ix_pp = sum(
            [self.num_r1_ix_pp, self.num_r2_ix_pp, self.num_r3_ix_pp]
            )

        self.sec_per_r1_ix = SEC_PER_R1_IX
        self.sec_per_r2_ix = SEC_PER_R2_IX
        self.sec_per_r3_ix = SEC_PER_R3_IX

        self.sec_in_r1 = self.num_r1_ix_pp * self.sec_per_r1_ix
        self.sec_in_r2 = self.num_r2_ix_pp * self.sec_per_r2_ix
        self.sec_in_r3 = self.num_r3_ix_pp * self.sec_per_r3_ix
        self.sec_in_event = sum(
            [self.sec_in_r1, self.sec_in_r2, self.sec_in_r3]
            )

        self.li_sta_nums = range(1, self.num_stations + 1)
        self.li_sub_nums = range(1, self.num_stations + 1)
        self.li_m_ipad_nums = range(1, self.num_stations + 1)
        self.li_f_ipad_nums = range(self.num_stations+1, 2*self.num_stations+1)
        self.li_q_nums = range(1, self.num_stations + 1)

        # Create event-user (zE0000_User) objects in Parse.
        self.li_eu = self.create_event_users_in_Parse()

        eu_cls_name = "zE" + self.event_serial + "_User"
        eu_cls = Object.factory(eu_cls_name)
        euq = eu_cls.Query.all().limit(1000)
        self.li_meup = list(euq.filter(sex = "M").order_by("euNum"))
        self.li_feup = list(euq.filter(sex = "F").order_by("euNum"))
        self.li_meug = list(euq.filter(sex = "MG").order_by("euNum"))
        self.li_feug = list(euq.filter(sex = "FG").order_by("euNum"))
        self.li_all_meu = self.li_meup + self.li_meug
        self.li_all_feu = self.li_feup + self.li_feug
        self.li_all_eu = self.li_all_meu + self.li_all_feu
        self.li_all_eu.sort(key = lambda x: x.euNum)
        print(len(self.li_all_eu))

        ipq = IPad.Query.all().limit(self.num_ipads).order_by("iPadNum")
        m_ipq = ipq.limit(self.num_stations).order_by("iPadNum")
        f_ipq = ipq.skip(self.num_stations).limit(self.num_stations)
        f_ipq = f_ipq.order_by("iPadNum")
        self.li_m_ipad_objs = list(m_ipq)
        self.li_f_ipad_objs = list(f_ipq)

        self.li_q_objs = Question.Query.all().limit(1000).order_by("qNum")

        self.start_at_round = START_AT_ROUND
        self.curr_rd = START_AT_ROUND

        #########   END INSTANCE VARIABLES   ##########

        # Create a corresponding Event object in Parse.
        self.create_event_object_in_Parse()

        # Create a skeleton DB in Firebase
        self.create_QA_and_SAC_databases_in_Firebase()

        pass


    def set_Parse_specific_global_classes(self, eNum):

        serial = mk_serial(eNum)
        str_event_user_class_name = "zE" + serial + "_User"
        str_r1_ix_class_name = "zE" + serial + "R1_Ix"
        str_r2_ix_class_name = "zE" + serial + "R2_Ix"
        str_r3_ix_class_name = "zE" + serial + "R3_Ix"
        cls_EventUser = Object.factory(str_event_user_class_name)
        cls_R1Ix = Object.factory(str_r1_ix_class_name)
        cls_R2Ix = Object.factory(str_r2_ix_class_name)
        cls_R3Ix = Object.factory(str_r3_ix_class_name) 

        pass


    def create_event_object_in_Parse(self):
        # Create a corresponding Event object in Parse upon initialization.
        pe = Event() # Remember, this is a Parse Event object, so it's ok
                    # to do this from inside _Event!
        pe.eventNum = self.event_number
        pe.eventSerial = self.event_serial
        pe.location = self.event_location
        pe.start = [self.event_date, self.event_time]
        pe.startDate = self.event_date
        pe.startTime = self.event_time
        pe.numMen = self.num_m_eu_p
        pe.numWomen = self.num_f_eu_p
        pe.numPeople = sum([self.num_m_eu_p, self.num_f_eu_p])
        pe.numMaleGhosts = self.num_m_eu_g
        pe.numFemaleGhosts = self.num_f_eu_g
        pe.numGhosts = sum([self.num_m_eu_g, self.num_f_eu_g])
        pe.numStations = self.num_stations
        pe.numIPads = self.num_ipads
        pe.save()

        pass


    def create_event_users_in_Parse(self):

        # For now, just grab first ones; later, check by array_eventsRegistered.

        """
        Create zE0000_User objects by "batch_save"-ing them to Parse using 
        ParsePy's ParseBatcher(). Event User objects are _User objects whose 
        array_eventsRegistered contains the eventNum of this current event.

        """

        eu_ClassName = "zE" + self.event_serial + "_User"
        eu_Class = Object.factory(eu_ClassName)

        # add some Users to e, which is this event
        qset_all_users = User.Query.all().order_by("userNum")
        li_meu = list(qset_all_users.filter(sex = "M").limit(self.num_m_eu_p))
        li_feu = list(qset_all_users.filter(sex = "F").limit(self.num_f_eu_p))
        li_mgeu = list(qset_all_users.filter(sex = "MG").limit(self.num_m_eu_g))
        li_fgeu = list(qset_all_users.filter(sex = "FG").limit(self.num_f_eu_g))

        li_users_at_event = li_meu + li_feu + li_mgeu + li_fgeu

        li_eu_obj_to_upload = []


        for index, User_object in enumerate(li_users_at_event):
            new_EU_object = eu_Class(
                userObjectId = User_object.objectId,
                euNum = index + 1,
                username = User_object.username,
                first = User_object.username.split(" ")[0],
                last = User_object.username.split(" ")[-1],
                sex = User_object.sex
                )
            li_eu_obj_to_upload.append(new_EU_object)


        # Batch upload in chunks no larger than 50, and sleep to avoid timeouts
        batch_upload_to_Parse(eu_ClassName, li_eu_obj_to_upload)    

        return li_eu_obj_to_upload


    def create_QA_and_SAC_databases_in_Firebase(self):
        pass


################################################################################
"""                                  _ROUND                                  """
################################################################################

class _Round(Object):

    def __init__(self, e):

        # # Initialize the round_num variable (Round_3 will set it to 3, for ex.)
        # self.round_num = None

        # # Initialize the sec_per_ix variable (differs by round)
        # self.sec_per_ix = None

        # # Initialize the round_time variable (equals #stations * sec_per_ix)
        # self.sec_in_round = None

        # # Fill the class list of event users.
        # _Round.LI_EVENT_USERS = list(
        #     cls_EventUser.Query.all().limit(1000).order_by("euNum"))

        # # Refresh the global list of event users
        # LI_EVENT_USERS = _Round.LI_EVENT_USERS


        """ Set instance variables. """

        self.e = e # proper and allows access to e without having to pass it

        self.event_number = e.event_number

        self.curr_rd = e.curr_rd

        if self.curr_rd == 1:
            str_r1_ix_class_name = "zE" + e.event_serial + "R1_Ix"
            cls_R1Ix = Object.factory(str_r1_ix_class_name)
            self.cls = cls_R1Ix
            self.str_cls = str_r1_ix_class_name
            self.num_ix_pp = e.num_r1_ix_pp
            self.sec_per_ix = e.sec_per_r1_ix
        elif self.curr_rd == 2:
            str_r2_ix_class_name = "zE" + e.event_serial + "R2_Ix"
            cls_R2Ix = Object.factory(str_r2_ix_class_name)
            self.cls = cls_R2Ix
            self.str_cls = str_r2_ix_class_name
            self.num_ix_pp = e.num_r2_ix_pp
            self.sec_per_ix = e.sec_per_r2_ix
        elif self.curr_rd == 3:
            str_r3_ix_class_name = "zE" + e.event_serial + "R1_3x"
            cls_R3Ix = Object.factory(str_r3_ix_class_name)
            self.cls = cls_R3Ix
            self.str_cls = str_r3_ix_class_name
            self.num_ix_pp = e.num_r3_ix_pp
            self.sec_per_ix = e.sec_per_r3_ix
        else:
            self.num_ix_pp = 0
            self.sec_per_ix = 0

        self.num_ix_in_round = self.num_ix_pp * e.num_stations
        self.sec_in_round = self.num_ix_in_round * self.sec_per_ix


        """ Do stuff. """

        self.create_round_object_in_Parse()

        self.li_ix_in_round = []

        # if self.curr_rd in [1, 2, 3]:
        #     self.li_ix_in_round = self.create_ix_objects_in_Parse()

        pass

    def create_round_object_in_Parse(self):
        # Will be called inside the initiator of Round_0, Round_1, etc.
        pr = Round()
        pr.eventNum = self.event_number
        pr.roundNum = self.curr_rd
        pr.numIxPP = self.num_ix_pp
        pr.numIxInRound = self.num_ix_in_round
        pr.secPerIx = self.sec_per_ix
        pr.secInRound = self.sec_in_round 
        pr.save()
        pass

    def create_ix_objects_in_Parse(self):
        # Queries Parse for all event users, and, depending on which round
        # it is, creates a different number of Interaction objects in Parse

        li_ix_to_up = []

        # create num_ix_in_round ix objects in Parse, keep a global list here too.
        # iterate first through subrounds, then through male event users
        # ...using a list comprehension!
        # Source: https://www.safaribooksonline.com/library/view/python-cookbook/0596001673/ch01s15.html
        for sr, (index, meu) in [(sr, (index, meu)) for sr in range(1, self.num_ix_pp + 1) for index, meu in enumerate(self.e.li_all_meu)]:
            ix = self.cls()
            ix.ixNum = ((sr - 1) * self.e.num_stations) + (index+1) # Ex: ((1 - 1) * 51 + 9) = 9
            ix.subNum = sr
            ix.staNum = index + 1
            ix.mEventUserNum = None
            ix.fEventUserNum = None
            ix.qNum = None
            ix.mUsername = None
            ix.fUsername = None
            ix.mNextStaNum = None
            ix.fNextStaNum = None
            ix.mIpadNum = None
            ix.fIpadNum = None
            ix.mUserNum = None
            ix.fUserNum = None
            ix.mUserObjectId = None
            ix.fUserObjectId = None
            ix.mEventUserObjectId = None
            ix.fEventUserObjectId = None
            li_ix_to_up.append(ix)

        print(len(li_ix_to_up))

        """     
        ### Rotate the lists between subrounds (in "for j in range(s)" loop).
        ###   (li_staNum will be iterated through correctly without alteration,
        ###   as will the lists of ipadNums.)

        # the m list will have its last item put in the front
        li_males = [li_males[-1]] + li_males[:-1]

        [m1, m2, m3, ..., m49, m50, m51]
        [m51, m1, m2, ..., m48, m49, m50]

        # the f list will have its first item put in the back
        li_females = li_females[1:] + [li_females[0]]

        [f1, f2, f3, ..., f49, f50, f51]
        [f2, f3, f4, ..., f50, f51, f1]

        # the qNums list happens to move the first two to the back
        li_qNums = li_qNums[2:] + li_qNums[:2]  

        [q1, q2, q3, ..., q49, q50, q51]
        [q3, q4, q5, ..., q51, q1, q2]

        """

        # batch upload in chunks to avoid timout in Sublime builds(?)
        if self.num_ix_in_round < 1000:
            batch_upload_to_Parse(self.str_cls, li_ix_to_up)
        else: 
            if self.num_ix_in_round < 2000:
                batch_upload_to_Parse(self.str_cls, li_ix_to_up[:1000])
                batch_upload_to_Parse(self.str_cls, li_ix_to_up[1000:])
            else:
                batch_upload_to_Parse(self.str_cls, li_ix_to_up[:1000])
                batch_upload_to_Parse(self.str_cls, li_ix_to_up[1000:2000])
                batch_upload_to_Parse(self.str_cls, li_ix_to_up[2000:])

        # # fill global list of this round's interaction objects
        # # 24 is my favorite number! And is completely random/immaterial here.
        # for index, li in enumerate([24, LI_R1_IX, LI_R2_IX, LI_R3_IX]):
        #     if self.curr_rd == index:
        #         li = li_ix_to_up
        #         print (len(li), len(li_ix_to_up))
        # print(len(LI_R1_IX), len(LI_R2_IX), len(LI_R3_IX))

        return li_ix_to_up

    def prepare(self):
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

    def __init__(self, e):
        _Round.__init__(self, e)
        self.round_num = 0
        pass

    def assign_pregame_sel_and_des_ranks(self):
        pass

    # def prepare(self):
    #     self.assign_pregame_sel_and_des_ranks()

    #     pass

    # def simulate(self): 
    #     # nothing to do here
    #     pass

    # def analyze(self):
    #     pass

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

    def __init__(self, e):
        _Round.__init__(self, e)
        self.round_num = 1
        pass

    def prepare(self):
        # make and upload to Parse all MEN * WOMEN interaction objects
        self.li_ix_in_round = self.create_ix_objects_in_Parse()

        pass

    # def simulate(self):
    #     pass

    # def analyze(self):
    #     pass

    pass

###############################################################################
"""                               Round 2                                   """
###############################################################################

class Round_2(_Round):

    def __init__(self, e):
        _Round.__init__(self, e)
        self.round_num = 2
        pass

    def prepare(self):
        self.li_ix_in_round = self.create_ix_objects_in_Parse()

        pass

    # def simulate(self):
    #     pass

    # def analyze(self):
    #     pass

    pass

###############################################################################
"""                               Round 3                                   """
###############################################################################

class Round_3(_Round):

    def __init__(self, e):
        _Round.__init__(self, e)
        self.round_num = 3
        pass

    def prepare(self):
        self.li_ix_in_round = self.create_ix_objects_in_Parse()
        pass

    # def simulate(self):
    #     pass

    # def analyze(self):
    #     pass

    pass

###############################################################################
"""                               Round 4                                   """
###############################################################################

class Round_4(_Round):
    """
    Postgame stuff.
    """

    def __init__(self, e):
        _Round.__init__(self, e)
        self.round_num = 4
        pass

    # def prepare(self):
    #     pass

    # def simulate(self):
    #     pass

    # def analyze(self):
    #     pass

    pass


################################################################################
"""                               _INTERACTION                               """
################################################################################

class _Interaction(Object):

    COUNTER = 0

    def __init__(self, e, r):
        _Interaction.COUNTER += 1
        self.ixNum = _Interaction.COUNTER
        self.event_serial = e.event_serial
        self.create_Ix_Object_in_Parse()

    def create_Ix_Object_in_Parse(self):
        Cls_EU = Object.factory("zE" + e.event_serial + "R" + str(CURRENT_ROUND))
        self.ix = Cls_EU()
        self.ix.save()


    def simulate(self):
        mSeeF = random.choice(["no", "maybe-no", "maybe-yes", "yes"])
        pass

    pass

################################################################################
"""                                  _USER                                   """
################################################################################

################################################################################
"""                                _QUESTION                                 """
################################################################################

################################################################################
"""                                SIMULATE                                 """
################################################################################

def simulate(e):
    # simulates an entire event (all 3 rounds, plus pregame and postgame)

    r0 = Round_0(e) if e.start_at_round <= 0 else 0
    e.curr_rd += 1
    r1 = Round_1(e) if e.start_at_round <= 1 else 0
    e.curr_rd += 1
    r2 = Round_2(e) if e.start_at_round <= 2 else 0
    e.curr_rd += 1
    r3 = Round_3(e) if e.start_at_round <= 3 else 0
    e.curr_rd += 1
    r4 = Round_4(e) if e.start_at_round <= 4 else 0

    # print("\n{} Round objects created.".format([r0,r1,r2,r3,r4])))

    for r in [r0, r1, r2, r3, r4]:
        if isinstance(r, _Round):
            print("\nCurrent Round:", r.round_num)
            r.prepare()
            r.simulate()
            r.analyze()
   
    pass

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
    2. Delete all objects in desired general classes from Parse.
    3. Set the Parse event-specific global classes.
    4. Delete all objects in desired event-specific classes from Parse.
    5. Create an _Event object.
    6. Simulate event.
    7. Run tests on results.
    """

    """  1. Register with Parse.  """
    register_with_Parse() 


    """  2. Delete all objects in desired general classes from Parse.  """
    ## (Maintain sanity when testing.)
    ## (The for: loop should work too, but if I want to save time when testing,
    ## I can comment out individual lines, so that's how I've kept them)
    # for cls in ["Event", "Round", "zE_0000_User", "zE_0000_R1", "zE_0000_R2", 
    # "zE_0000_R3"]:
    #     batch_delete_from_Parse_all_objects_of_class(cls)
    batch_delete_from_Parse_all_objects_of_class("Event")
    batch_delete_from_Parse_all_objects_of_class("Round")


    """  3. Set the Parse event-specific global classes.   """
    #e.set_Parse_specific_global_classes(e.event_number)

    EVENT_NUMBER = 0
    serial = mk_serial(EVENT_NUMBER)
    str_event_user_class_name = "zE" + serial + "_User"
    str_r1_ix_class_name = "zE" + serial + "R1_Ix"
    str_r2_ix_class_name = "zE" + serial + "R2_Ix"
    str_r3_ix_class_name = "zE" + serial + "R3_Ix"
    cls_EventUser = Object.factory(str_event_user_class_name)
    cls_R1Ix = Object.factory(str_r1_ix_class_name)
    cls_R2Ix = Object.factory(str_r2_ix_class_name)
    cls_R3Ix = Object.factory(str_r3_ix_class_name) 


    """  4. Delete all objects in event-specific classes from Parse.  """

    batch_delete_from_Parse_all_objects_of_class(str_event_user_class_name)
    batch_delete_from_Parse_all_objects_of_class(str_r1_ix_class_name)
    batch_delete_from_Parse_all_objects_of_class(str_r2_ix_class_name)
    batch_delete_from_Parse_all_objects_of_class(str_r3_ix_class_name)


    """  5. Create an _Event object.  """
    e = _Event(
        EVENT_NUMBER = 0,
        MEN = 20,
        WOMEN = 20,
        START_AT_ROUND = 0,
        SEC_PER_R1_IX = 20,
        SEC_PER_R2_IX = 40,
        SEC_PER_R3_IX = 60
        )


    """  6. Simulate event.  """
    # . Simulate the entire event.
    simulate(e)



    # 4. Run tests on the results.

    pass


if __name__ == '__main__':
    status = main()
    print("\n---\n\ndaeious.py has finished running.\n")
    sys.exit(status)































