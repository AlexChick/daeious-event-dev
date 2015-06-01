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

# # Import backoff, which avoids timeouts
import backoff

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

        # Create event-user (zE0000_User) objects in Parse.
        #  self.li_eu = self.create_event_users_in_Parse()

        
        # euq = batch_query(
        #     Source = "Parse",
        #     Cls = eu_cls,
        #     Limit = self.num_all_eu,
        #     OrderBy = "euNum")
        # #euq = eu_cls.Query.all().limit(1000)
        # self.li_meup = list(euq.filter(sex = "M"))
        # self.li_feup = list(euq.filter(sex = "F"))
        # self.li_meug = list(euq.filter(sex = "MG"))
        # self.li_feug = list(euq.filter(sex = "FG"))
        # self.li_all_meu = self.li_meup + self.li_meug
        # self.li_all_feu = self.li_feup + self.li_feug
        # self.li_all_eu = self.li_all_meu + self.li_all_feu
        # self.li_all_eu.sort(key = lambda x: x.euNum)

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
        # self.li_m_ipad_objs = list(m_ipq)
        # self.li_f_ipad_objs = list(f_ipq)

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
        #self.li_q_objs = list(Question.Query.all().limit(self.num_stations).order_by("qNum"))


        self.start_at_round = START_AT_ROUND
        self.curr_rd = START_AT_ROUND

        #########   END INSTANCE VARIABLES   ##########

        # Create a corresponding Event object in Parse.
        #  self.create_event_object_in_Parse()

        # Create a skeleton DB in Firebase
        self.create_QA_and_SAC_databases_in_Firebase()

        pass


    # def create_event_object_in_Parse(self):
    #     # Create a corresponding Event object in Parse upon initialization.
    #     pe = Event() # Remember, this is a Parse Event object, so it's ok
    #                 # to do this from inside _Event!
    #     pe.eventNum = self.event_number
    #     pe.eventSerial = self.event_serial
    #     pe.location = self.event_location
    #     pe.start = [self.event_date, self.event_time]
    #     pe.startDate = self.event_date
    #     pe.startTime = self.event_time
    #     pe.numMen = self.num_m_eu_p
    #     pe.numWomen = self.num_f_eu_p
    #     pe.numPeople = sum([self.num_m_eu_p, self.num_f_eu_p])
    #     pe.numMaleGhosts = self.num_m_eu_g
    #     pe.numFemaleGhosts = self.num_f_eu_g
    #     pe.numGhosts = sum([self.num_m_eu_g, self.num_f_eu_g])
    #     pe.numStations = self.num_stations
    #     pe.numIPads = self.num_ipads
    #     pe.save()

    #     pass


    # def create_event_users_in_Parse(self):

    #     """
    #     Create zE0000_User objects by "batch_save"-ing them to Parse using 
    #     ParsePy's ParseBatcher(). Event User objects are _User objects whose 
    #     array_eventsRegistered contains the eventNum of this current event.

    #     """

    #     qset_all_users = User.Query.all().order_by("userNum")
    #     li_meup = list(qset_all_users.filter(sex = "M").limit(self.num_m_eu_p))
    #     li_feup = list(qset_all_users.filter(sex = "F").limit(self.num_f_eu_p))
    #     li_meug = list(qset_all_users.filter(sex = "MG").limit(self.num_m_eu_g))
    #     li_feug = list(qset_all_users.filter(sex = "FG").limit(self.num_f_eu_g))

    #     li_users_at_event = li_meup + li_feup + li_meug + li_feug

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

    def __init__(self, e):

        # # Initialize the round_num variable (Round_3 will set it to 3, for ex.)
        # self.round_num = None

        # # Fill the class list of event users.
        # _Round.LI_EVENT_USERS = list(
        #     cls_EventUser.Query.all().limit(1000).order_by("euNum"))

        # # Refresh the global list of event users
        # LI_EVENT_USERS = _Round.LI_EVENT_USERS


        """ Set instance variables. """

        self.e = e # proper and allows access to e in functions 
                   # without having to pass it

        self.event_number = e.event_number

        self.curr_rd = e.curr_rd

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


        """ Do stuff. """

        self.li_ix_in_round = []

        # if self.curr_rd in [1, 2, 3]:
        #     self.li_ix_in_round = self.create_ix_objects_in_Parse()

        pass

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

class _Interaction(object):

    COUNTER = 0

    def __init__(self, e, r):
        _Interaction.COUNTER += 1
        self.e = e
        self.r = r
        self.ix_num = _Interaction.COUNTER

    def simulate(self):
        self.m_see_f = random.choice(["no", "maybe-no", "maybe-yes", "yes"])
        self.f_see_m = random.choice(["no", "maybe-no", "maybe-yes", "yes"])
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

    """  Create 5 _Round objects.  """

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

    """  Simulate the rounds.  """
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
    1. Create fake users, ghosts, ipads, questions from helper functions
    5. Create and simulate an event by calling simulate()
    7. Run tests on results.
    """

    start = time.time()

    """  Create 1 _Event object.  """
    e = _Event(
        EVENT_NUMBER = 0,
        MEN = 12,
        WOMEN = 12,
        START_AT_ROUND = 0,
        SEC_PER_R1_IX = 20,
        SEC_PER_R2_IX = 40,
        SEC_PER_R3_IX = 60
        )

    """  Simulate event.  """
    simulate(e)



    # 4. Run tests on the results.

    end = time.time()

    return round(end-start, 2)


if __name__ == '__main__':
    logging.getLogger('backoff').addHandler(logging.StreamHandler())
    start = time.time()
    status = main()
    print("\n---\n\ndaeious.py has finished running in {} seconds.\n".format(
        round(time.time() - start, 2)))
    sys.exit(status)































