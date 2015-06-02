"""
This program simulates a Daeious event from start to finish,
and runs tests that assess a "satisfaction" score of the algorithm's
choices for which interactions happen again.

I define "satisfaction" here as a person's (simulated) IRL response to the 
pairings they receive in R2 and R3. Did they really really like someone, and
was really really liked by that same someone, and yet they didn't get an
interaction with them in the next round? That's the opposite of satisfaction.

For each person, a satisfaction score (0-100) represents how close they were
to getting exactly what they wanted in R2 and R3. The higher the average 
of these "satisfactions", the better the algorithm. Initially, I can think 
of several ways of pairing people (choosing which pairings happen again), 
but I won't really be able to know which is best unless I run 1000's of events 
with each and compare their average event satisfaction scores.

Why does a high satisfaction score matter so much? Because it means that the
algorithm is as close to being a good "matchmaker" / "pairer" as possible.

Questions I'm pondering:

-- Should there be a way to "star" a person who you absolutely 
HAVE to see again? That would give added "power" to the interaction.

-- Should Facebook data be used to match people with, for instance, similar
taste in music? Doing so would require people to connect Daeious with their
Facebook accounts, which I'm not sure everyone would do. So I guess that's
something for down the road.

-- Is sec_per_ix something that will change according to how events go?
Probably. But I should still have some rules -- like, if I want every single
event to be 1 hour, how are things different when there are 40 ppl vs. 100 ppl?
Maybe 20m/20w events will just have to be shorter. How much shorter? I can
figure that out by scaling down how I want a 50m/50w event to be structured.
    - Given 50m/50w/1mg/1fg,
        R1 --> sec_per_r1_ix = 15 --> 51 * 15 = 765s = 12.75min = 12m45s.
               sec_per_r1_ix = 20 --> 51 * 20 = 1020s = 17.00min = 17m00s.
               sec_per_r1_ix = 25 --> 51 * 25 = 1275s = 21.25min = 21m15s.
               sec_per_r1_ix = 30 --> 51 * 30 = 1530s = 25.50min = 25m30s.

        R2 --> sec_per_r2_ix = 30 --> 12 * 030 = 360s = 06.00min = 06m 00s.
               sec_per_r2_ix = 40 --> 12 * 040 = 480s = 08.00min = 08m 00s.
               sec_per_r2_ix = 45 --> 12 * 045 = 540s = 09.00min = 09m 00s.
               sec_per_r2_ix = 50 --> 12 * 050 = 600s = 10.00min = 10m 00s.
               sec_per_r2_ix = 60 --> 12 * 060 = 720s = 12.00min = 12m 00s.

        R3 --> sec_per_r3_ix = 60 --> 05 * 060 = 300s = 05.00min = 05m 00s.
               sec_per_r3_ix = 80 --> 05 * 080 = 400s = 06.66min = 06m 40s.
               sec_per_r3_ix = 90 --> 05 x 090 = 450s = 07.50min = 07m 30s.
               sec_per_r3_ix = 100 -> 05 * 100 = 500s = 08.33min = 08m 20s.
               sec_per_r3_ix = 120 -> 05 * 120 = 600s = 10.00min = 10m 00s.
               sec_per_r3_ix = 135 -> 05 * 135 = 675s = 11.25min = 11m 15s.
               sec_per_r3_ix = 180 -> 05 * 180 = 900s = 15.00min = 15m 00s.

    - Event length (without between-round breaks or pre- or post-game talks):
        -- Doubling --
        (15, 30, 60) --> 23m 45s
        (20, 40, 80) --> 31m 40s
        (25, 50, 100) -> 39m 35s
        (30, 60, 120) -> 47m 30s
        -- Tripling -- 
        (15, 45, 135) -> 33m 00s
        (20, 60, 180) -> 44m 00s
        -- Other --
        (15, 45, 100)
        (15, 45, 120)
        (15, 60, 120)
        (15, 60, 150)
        (15, 60, 180)
        (20, 45, )



sec_per_ix: 
    - (Should Round_1 be a constant number of minutes, so that interactions
        are longer when there are fewer people? Or should the sec_per_ix
        be a constant for each round? I'll have to play around with that.
        Right now, I'm leaning towards keeping sec_per_ix constant.)


"""


# Import Python stuff.
from __future__ import print_function # apparently, has to be on first line
from pprint import pprint
import itertools
import logging
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

# Import custom modules, mostly from GitHub
import backoff
import xlwt

# Import custom functions and classes I've written specifically for Daeious.
#from helpers import batch_delete_from_Parse_all_objects_of_class
#from helpers import batch_query
#from helpers import batch_upload_to_Parse
from helpers import create_QA_database_in_Firebase
from helpers import create_SAC_database_in_Firebase
from helpers import filter_by_value
from helpers import mk_serial

################################################################################
################################################################################
################################################################################
###                                                                          ###
"""                                 GLOBALS                                  """
###                                                                          ###
################################################################################
################################################################################
################################################################################




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

class _Event(object): 

    def __init__(self, EVENT_NUMBER = 0,
                       START_AT_ROUND = 0,
                       MEN = 20,
                       WOMEN = 20,
                       SEC_PER_R1_IX = 20,
                       SEC_PER_R2_IX = 40,
                       SEC_PER_R3_IX = 60
        ):

        # You CAN'T SET GLOBALS from within __init__ 
        # But you CAN assign to self.whatever

        # Set instance variables
        self.event_number = EVENT_NUMBER
        self.event_serial = mk_serial(EVENT_NUMBER)
        self.event_date = time.strftime("%Y.%m.%d")
        self.event_time = random.choice(["19:00", "19:30", "20:00", "20:30"])
        self.event_location = random.choice(["Heaven", "California"])

        self.max_sex = max(MEN,WOMEN)
        self.num_stations = self.max_sex if self.max_sex%2==1 else self.max_sex+1
        self.num_ipads = self.num_stations * 2

        self.num_m_eu_p = MEN
        self.num_f_eu_p = WOMEN
        self.num_all_eu_p = MEN + WOMEN

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
        self.num_r1_ix = self.max_sex*self.num_r1_ix_pp
        self.num_r2_ix = self.max_sex*self.num_r2_ix_pp
        self.num_r3_ix = self.max_sex*self.num_r3_ix_pp
        self.num_event_ix = sum(
            [self.num_r1_ix, self.num_r2_ix, self.num_r3_ix]
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

        # Create event-user objects.
        self.li_eu = self.get_event_users()

        
        # self.li_mpeu = 
        # self.li_fpeu = 
        # self.li_mgeu = 
        # self.li_fgeu = 
        # self.li_all_meu = self.li_mpeu + self.li_mgeu
        # self.li_all_feu = self.li_fpeu + self.li_fgeu
        # self.li_all_eu = self.li_all_meu + self.li_all_feu
        # self.li_all_eu.sort(key = lambda x: x.eu_num)

        # self.li_m_ipad_objs = list(m_ipq)
        # self.li_f_ipad_objs = list(f_ipq)

        # self.li_q_objs = list(Question.Query.all().limit(self.num_stations).order_by("qNum"))


        # m_ipq = batch_query(
        #     Source = "Parse",
        #     Cls = IPad,
        #     Limit = self.num_stations,
        #     OrderBy = "ipNum"
        #     )
        # f_ipq = batch_query(
        #     Source = "Parse",
        #     Cls = IPad,
        #     Limit = self.num_stations,
        #     OrderBy = "ipNum",
        #     Skip = self.num_stations
        #     )
        #ipq = IPad.Query.all().limit(self.num_ipads).order_by("iPadNum")
        # m_ipq = ipq.limit(self.num_stations).order_by("iPadNum")
        # f_ipq = ipq.skip(self.num_stations).limit(self.num_stations)
        # f_ipq = f_ipq.order_by("iPadNum")

        # self.li_q_objs = list(batch_query(
        #     Source = "Parse",
        #     Cls = Question,
        #     Filter = ["qNum", "<=", self.num_event_ix_pp],
        #     Limit = self.num_event_ix_pp,
        #     OrderBy = "qNum"
       #  #     ))
       # # self.li_q_objs = list(
       #      Question.Query.all()
       #                    .order_by("qNum")
       #                    .filter(qNum__lte = self.num_event_ix_pp)
       #      )
       #  # self.li_q_objs = list(qq)


        self.start_at_round = START_AT_ROUND

        #########   END INSTANCE VARIABLES   ##########

        # Create a corresponding Event object in Parse.
        #  self.create_event_object_in_Parse()

        # Create a skeleton DB in Firebase
        self.create_QA_and_SAC_databases_in_Firebase()

        pass

    def get_event_users(self):
        """
        Returns a list of the desired event users.
        """
        pass




    # def create_event_users_in_Parse(self):

    #     """
    #     Create zE0000_User objects by "batch_save"-ing them to Parse using 
    #     ParsePy's ParseBatcher(). Event User objects are _User objects whose 
    #     array_eventsRegistered contains the eventNum of this current event.

    #     """

    #     qset_all_users = User.Query.all().order_by("userNum")
    #     li_mpeu = list(qset_all_users.filter(sex = "M").limit(self.num_m_eu_p))
    #     li_fpeu = list(qset_all_users.filter(sex = "F").limit(self.num_f_eu_p))
    #     li_mgeu = list(qset_all_users.filter(sex = "MG").limit(self.num_m_eu_g))
    #     li_fgeu = list(qset_all_users.filter(sex = "FG").limit(self.num_f_eu_g))

    #     li_users_at_event = li_mpeu + li_fpeu + li_mgeu + li_fgeu

    #     li_eu_obj_to_upload = []

    #     for index, User_object in enumerate(li_users_at_event):
    #         new_EU_object = eu_Class(
    #             userObjectId = User_object.objectId,
    #             euNum = index + 1,
    #             userNum = User_object.userNum,
    #             username = User_object.username,
    #             first = User_object.username.split(" ")[0],
    #             last = User_object.username.split(" ")[-1],
    #             sex = User_object.sex
    #             )
    #         li_eu_obj_to_upload.append(new_EU_object)


    #     # Batch upload in chunks no larger than 50, and sleep to avoid timeouts
    #     batch_upload_to_Parse(eu_ClassName, li_eu_obj_to_upload)    

    #     return li_eu_obj_to_upload


    def create_QA_and_SAC_databases_in_Firebase(self):
        pass


################################################################################
"""                                  _ROUND                                  """
################################################################################

class _Round(object):

    CURR_ROUND = -1

    def __init__(self, e):

        _Round.CURR_ROUND += 1

        # # Fill the class list of event users.
        # _Round.LI_EVENT_USERS = list(
        #     cls_EventUser.Query.all().limit(1000).order_by("euNum"))

        # # Refresh the global list of event users
        # LI_EVENT_USERS = _Round.LI_EVENT_USERS


        """ Set instance variables. """

        self.e = e # proper and allows access to e in functions 
                   # without having to pass it

        self.event_number = e.event_number

        self.curr_rd = _Round.CURR_ROUND

        if self.curr_rd == 1:
            self.num_ix_pp = e.num_r1_ix_pp
            self.sec_per_ix = e.sec_per_r1_ix
        elif self.curr_rd == 2:
            self.num_ix_pp = e.num_r2_ix_pp
            self.sec_per_ix = e.sec_per_r2_ix
        elif self.curr_rd == 3:
            self.num_ix_pp = e.num_r3_ix_pp
            self.sec_per_ix = e.sec_per_r3_ix
        else:
            self.num_ix_pp = 0
            self.sec_per_ix = 0

        self.num_ix_in_round = self.num_ix_pp * e.num_stations
        self.sec_in_round = self.num_ix_in_round * self.sec_per_ix

        pass

    def prepare(self):
        pass

    def simulate(self, li = []):
        """
        Take a list of interaction objects to simulate.
        Return the same list, with updated values.
        """

        if li: # equivalent to, and faster than, if li != []
            for ix in li:
                ix.m_see_f = random.randint(0,3) # 0 to 3 inclusive
                ix.f_see_m = random.randint(0,3)
                ix.quality = ix.m_see_f + ix.f_see_m
                ix.same_sac = (ix.m_see_f == ix.f_see_m)

        return li

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
    All men and all women have 1 interaction with each other,
    moving to their right by 1 iPad / station for each new interaction.
    """

    def __init__(self, e):
        _Round.__init__(self, e)
        self.round_num = 1
        pass
    pass

###############################################################################
"""                               Round 2                                   """
###############################################################################

class Round_2(_Round):

    def __init__(self, e):
        _Round.__init__(self, e)
        self.round_num = 2
        pass
    pass

###############################################################################
"""                               Round 3                                   """
###############################################################################

class Round_3(_Round):

    def __init__(self, e):
        _Round.__init__(self, e)
        self.round_num = 3
        pass
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
    pass


################################################################################
"""                               _INTERACTION                               """
################################################################################

class _Interaction(object):

    CURR_IX_NUM = 0

    def __init__(self, e, r, mEU, fEU):
        _Interaction.CURR_IX_NUM += 1
        self.e = e
        self.r = r
        self.round_num = r.round_num
        self.ix_num = _Interaction.CURR_IX_NUM
        self.m_eu_num = mEU.eu_num
        self.f_eu_num = fEU.eu_num
        self.simuate()

    def simulate(self):
        self.m_see_f = random.randint(0, 3)
        self.f_see_m = random.randint(0, 3)
        # self.m_see_f = random.choice(["no", "maybe-no", "maybe-yes", "yes"])
        # self.f_see_m = random.choice(["no", "maybe-no", "maybe-yes", "yes"])
        pass

    def __iter__(self):
        # first start by grabbing the Class items
        iters = dict((x,y) for x,y in _Interaction.__dict__.items() 
            if x[:2] != '__' 
                and x != "simulate"
                and x != "CURR_IX_NUM"
            )
        # then update the class items with the instance items
        iters.update(self.__dict__)
        # now 'yield' through the items
        for x,y in iters.items():
            yield x,y

    pass

################################################################################
"""                                  _USER                                   """
################################################################################

class _User(object):

    CURR_USER_NUM = 0

    def __init__(self):
        _User.CURR_USER_NUM += 1
        self.u_num = _User.CURR_USER_NUM
        if self.u_num <= 1000:
            self.sex = 'M'
        elif self.u_num <= 2000:
            self.sex = 'F'
        elif self.u_num <= 2100:
            self.sex = 'MG'
        elif self.u_num <= 2200:
            self.sex = 'FG'
        # else:
        #     raise ValueError("self.u_num {} is out of bounds.".format(self.u_num))
        pass

    def __iter__(self):
        # first start by grabbing the Class items
        iters = dict((x,y) for x,y in _User.__dict__.items() 
            if x[:2] != '__' 
                and x != "simulate"
                and x != "CURR_USER_NUM"
            )
        # then update the class items with the instance items
        iters.update(self.__dict__)
        # now 'yield' through the items
        for x,y in iters.items():
            yield x,y
    
    pass

################################################################################
"""                                _EVENTUSER                                 """
################################################################################

class _EventUser(_User):

    CURR_EVENTUSER_NUM = 0

    def __init__(self):
        _User.__init__(self)
        self.u_num -= 2200 # (because I added 2200 users)
        _EventUser.CURR_EVENTUSER_NUM += 1
        self.eu_num = _EventUser.CURR_EVENTUSER_NUM
        pass

    pass
################################################################################
"""                                  _IPAD                                   """
################################################################################

################################################################################
"""                                _QUESTION                                 """
################################################################################

################################################################################
"""                                SIMULATE                                 """
################################################################################

# def simulate(e):
#     # simulates an entire event (all 3 rounds, plus pregame and postgame)

#     """  Create 5 _Round objects.  """

#     r0 = Round_0(e) if e.start_at_round <= 0 else 0
#     r1 = Round_1(e) if e.start_at_round <= 1 else 0
#     r2 = Round_2(e) if e.start_at_round <= 2 else 0
#     r3 = Round_3(e) if e.start_at_round <= 3 else 0
#     r4 = Round_4(e) if e.start_at_round <= 4 else 0
#     print("\n{} Round objects created.".format(len([r0,r1,r2,r3,r4])))

#     """  Simulate the rounds.  """
#     for r in [r0, r1, r2, r3, r4]:
#         if isinstance(r, _Round):
#             print("\nCurrent Round:", r.round_num)
#             r.prepare()
#             r.simulate()
#             r.analyze()


   
#     pass

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
    1. Create fake users, ghosts, ipads, questions from helper functions
    5. Create and simulate an event by calling simulate()
    7. Run tests on results.
    """

    start = time.time()

    """  Create 1 _Event object.  """
    e = _Event(
        EVENT_NUMBER = 0,
        MEN = 50,
        WOMEN = 50,
        START_AT_ROUND = 0,
        SEC_PER_R1_IX = 20,
        SEC_PER_R2_IX = 40,
        SEC_PER_R3_IX = 60
        )

    """  Create Users: 1,000 men, 1,000 women, 100 male ghosts, 100 female ghosts.  """
    _User.CURR_USER_NUM = 0
    li_mpu = list((_User() for i in range(1000)))
    li_fpu = list((_User() for i in range(1000)))
    li_mgu = list((_User() for i in range(100)))
    li_fgu = list((_User() for i in range(100)))
    li_all_u = li_mpu + li_fpu + li_mgu + li_fgu


    """  Create correct number and type of EventUsers.  """
    ################
    ######   I THINK THIS IS WRONG.
    ######   I should be using li_mpu, li_fpu, etc to get correct eu_nums...shouldn't I?
    li_mpeu = list((_EventUser() for i in range(e.num_m_eu_p)))
    li_fpeu = list((_EventUser() for i in range(e.num_f_eu_p)))
    li_mgeu = list((_EventUser() for i in range(e.num_m_eu_g)))
    li_fgeu = list((_EventUser() for i in range(e.num_f_eu_g)))
    li_all_eu = li_mpeu + li_fpeu + li_mgeu + li_fgeu


    """  Create up to 5 _Round objects.  """
    r0 = Round_0(e) if e.start_at_round <= 0 else 0
    r1 = Round_1(e) if e.start_at_round <= 1 else 0
    r2 = Round_2(e) if e.start_at_round <= 2 else 0
    r3 = Round_3(e) if e.start_at_round <= 3 else 0
    r4 = Round_4(e) if e.start_at_round <= 4 else 0
    print("\n{} Round objects created.".format(len([r0,r1,r2,r3,r4])))

    """  Simulate the rounds.  """
    # simulates an entire event (all 3 rounds, plus pregame and postgame)

    li_r1_ix = []
    li_r2_ix = []
    li_r3_ix = []

    # li_r1_ix = r1.simulate(li_all_eu)
    li_r = [r0, r1, r2, r3, r4]
    li_li_ix_by_r = [0,li_r1_ix, li_r2_ix, li_r3_ix, 0]
    for r, (index, li) in zip(li_r, enumerate(li_li_ix_by_r)):
        if isinstance(r, _Round):
            print("\nCurrent Round:", r.round_num)
            r.prepare()
            li = r.simulate(li_all_eu)
            r.analyze()
            if index == 1:
                li_r1_ix = li
            elif index == 2:
                li_r2_ix = li
            else: # index == 3:
                li_r3_ix = li









    """  Create all sheets in Excel. """

    global WB
    WB = xlwt.Workbook()
    ws_User = WB.add_sheet('Users', cell_overwrite_ok = True)
    ws_EventUser = WB.add_sheet('Event Users', cell_overwrite_ok = True)
    ws_r1_ix = WB.add_sheet('R1 Ix', cell_overwrite_ok = True)
    ws_r2_ix = WB.add_sheet('R2 Ix', cell_overwrite_ok = True)
    ws_r3_ix = WB.add_sheet('R3 Ix', cell_overwrite_ok = True)

    #  Users

    # """  Write the column label names for the Users sheet in Excel  """
    # for c, label in enumerate(dict(li_mpu[0]).keys()):
    #         ws_User.write(0, c, label)

    """  Write the rows of Users in Excel (too early?)  """
    for c, label in enumerate(dict(li_all_u[0]).keys()):
        ws_User.write(0, c, label)
        for r, user in enumerate(li_all_u):
            ws_User.write(r+1, c, getattr(user, label))   

    #  Event Users

    # """  Write the column label names for the EventUsers sheet in Excel  """
    # for c, label in enumerate(dict(li_mpeu[0]).keys()):
    #         ws_EventUser.write(0, c, label)

    """  Write the rows of EventUsers in Excel (too early?)  """ # _EventUser
    for c, label in enumerate(dict(li_all_eu[0]).keys()): # for each attribute
        ws_EventUser.write(0, c, label) # make the column label in the first row
        for r, event_user in enumerate(li_all_eu): # for each EventUser
            ws_EventUser.write(r+1, c, getattr(event_user, label))

    #  R1_Ix

    for sheet, li in zip([ws_r1_ix, ws_r2_ix, ws_r3_ix], [li_r1_ix, li_r2_ix, li_r3_ix]): # for each round
        for c, label in enumerate(dict(li[0]).keys()): # for each column / attribute of an interaction
            sheet.write(0, c, label) # make the column label in the first row
            for r, ix in enumerate(li):
                sheet.write(r+1, c, getattr(ix, label))

    #  R2_Ix


    #  R3_Ix


    WB.save('example.xls')    


    # Run tests on the results.

    end = time.time()

    return round(end-start, 2)


if __name__ == '__main__':
    logging.getLogger('backoff').addHandler(logging.StreamHandler())
    start = time.time()
    status = main()
    print("\n---\n\ndaeious.py has finished running in {} seconds.\n".format(
        round(time.time() - start, 2)))
    sys.exit(status)































