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
import copy
import itertools
from itertools import chain
import logging
import math
import numpy # used for matrices for placing R2 and R3 ix's, and arange or linspace
import os
import random
import requests # required for firebase module
import sys
import time

# Import stuff that Parse might use.
import httplib, json, urllib

# Import ParsePy stuff. ParsePy makes using Parse in Python much easier.
from parse_rest.connection import ParseBatcher, register, SessionToken
from parse_rest.datatypes import ACL, Function, Object
from parse_rest.role import Role
from parse_rest.user import User

# Import Firebase stuff 
import requests

# Import custom modules, mostly from GitHub
from firebase import Firebase # https://github.com/mikexstudios/python-firebase
from mwmatching import maxWeightMatching # http://jorisvr.nl/maximummatching.html
import names # https://github.com/treyhunner/names
import backoff
import xlwt as excel

# Import custom functions and classes I've written specifically for Daeious.
#from helpers import batch_delete_from_Parse_all_objects_of_class
#from helpers import batch_query
#from helpers import batch_upload_to_Parse
from helpers import create_QA_database_in_Firebase
from helpers import create_SAC_database_in_Firebase
from helpers import filter_by_value
from helpers import guys_are_walking
from helpers import mk_serial
from helpers import optimize_event_timing
from helpers import xfrange

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
                       MEN = 50,
                       WOMEN = 50,
                       R2_IX_PP = 12,
                       R3_IX_PP = 4,
                       SEC_PER_R1_IX = 20,
                       SEC_PER_R2_IX = 40,
                       SEC_PER_R3_IX = 60
        ):

        # You CAN'T SET GLOBALS from within __init__ 
        # But you CAN assign to self.whatever

        # Set instance variables
        self.start_at_round = START_AT_ROUND
        self.event_num = EVENT_NUMBER
        self.event_serial = mk_serial(EVENT_NUMBER, 4)
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

        self.num_r1_ix_pp = self.num_stations
        self.num_r2_ix_pp = R2_IX_PP
        self.num_r3_ix_pp = R3_IX_PP
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

        pass

    def __repr__(self):
        return "{} {}".format(self.__class__.__name__, self.event_num)

    def __iter__(self):
        # first start by grabbing the Class items
        iters = dict((x,y) for x,y in _Event.__dict__.items() 
            if x[:2] != '__' 
                and x != "create_QA_and_SAC_databases_in_Firebase"
            )
        # then update the class items with the instance items
        iters.update(self.__dict__)
        # now 'yield' through the items
        for x,y in iters.items():
            yield x,y


################################################################################
"""                                  _ROUND                                  """
################################################################################

class _Round(object):

    CURR_ROUND = -1

    def __init__(self, e):

        _Round.CURR_ROUND += 1

        """ Set instance variables. """

        self.e = e # proper and allows access to e in functions 
                   # without having to pass it

        self.event_num = e.event_num

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



    def plan_A(self, leu, lix):
        """
        Take the highest-ranked ix's in lix from the previous round, 
        place them into e.num_r?_ix slots,
        and return a list of planned ix's, which is just an updated copy of lix.
        """
        return get_perfect_maximum_matchings(self.e, self, leu, lix)

###############################################################################
"""                               Round 0                                   """
###############################################################################
        

class Round_0(_Round):
    """
    --> Pregame stuff. Assume sufficient (>100) Users exist in Parse.
    """
    def __init__(self, e):
        _Round.__init__(self, e)
        self.round_num = 0
        pass
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



    def plan(self, leu):

        li_r1_ix_planned = []

        li_all_meu = [eu for eu in leu if eu.sex in ['M', 'MG']]
        li_all_feu = [eu for eu in leu if eu.sex in ['F', 'FG']]

        #print (self.e.li_sta_nums)
        #print ([x.eu_num for x in li_all_meu])

        for subround in range(1, self.e.num_r1_ix_pp+1):

            for n, station in enumerate(self.e.li_sta_nums):

                meu = li_all_meu[n]
                feu = li_all_feu[n]
                ix = _Interaction(self.e, self, meu, feu)
                ix.sub_num = subround
                ix.sta_num = station
                ix.q_num = self.e.li_q_nums[n]
                ix.m_ipad_num = self.e.li_m_ipad_nums[n]
                ix.f_ipad_num = self.e.li_f_ipad_nums[n]

                ix.m_hotness = meu.hotness
                ix.f_hotness = feu.hotness
                ix.m_nixness = meu.nixness
                ix.f_nixness = feu.nixness
                ix.m_personality = meu.personality
                ix.f_personality = feu.personality

                li_r1_ix_planned.append(ix)

            # Rotate the lists between subrounds.
            # The lists of station nums and m and f ipad nums
            # will be iterated through correctly without alteration.

            # the m list will have its last item put in the front
            li_all_meu = [li_all_meu[-1]] + li_all_meu[:-1]

            # the f list will have its first item put in the back
            li_all_feu = li_all_feu[1:] + [li_all_feu[0]]

            # the qNums list happens to move the first two to the back
            # ... But oops, doesn't work when num_q is divisible by 3.
            self.e.li_q_nums = self.e.li_q_nums[2:] + self.e.li_q_nums[:2] 

        return li_r1_ix_planned



    def simulate(self, lix):

        li_r1_ix_planned = lix

        li_no_count_by_eu = [0] * (self.e.num_all_eu+1)
        li_mn_count_by_eu = [0] * (self.e.num_all_eu+1)
        li_my_count_by_eu = [0] * (self.e.num_all_eu+1)
        li_yes_count_by_eu = [0] * (self.e.num_all_eu+1)
        lili_counts = [li_no_count_by_eu, li_mn_count_by_eu, li_my_count_by_eu, li_yes_count_by_eu]

        for ix in li_r1_ix_planned:

            ix.m_sac = random.randint(0,3)
            ix.f_sac = random.randint(0,3)
            
            # if (
            #     (lili_counts[0][ix.m_eu_num] >= 10 and ix.m_sac == 0) or
            #     (lili_counts[0][ix.f_eu_num] >= 10 and ix.f_sac == 0)):

            #     ix.m_sac = random.randint(1,3)
            #     ix.f_sac = random.randint(1,3)

            lili_counts[ix.m_sac][ix.m_eu_num] += 1
            lili_counts[ix.f_sac][ix.f_eu_num] += 1

            ix.sac_total = ix.m_sac + ix.f_sac
            ix.sac_same = 1 if ix.m_sac == ix.f_sac else 0

            ix.m_qa = random.choice(['A','B','C','D'])
            ix.f_qa = random.choice(['A','B','C','D'])
            ix.qa_same = 1 if ix.m_qa == ix.f_qa else 0
            ix.qa_likeness = None

        return li_r1_ix_planned # necessary?



    def analyze(self, leu, lix):

        li_r1_ix_analyzed = lix # DON'T modify li_r1_ix_simulated

        m_sel = 0
        f_sel = 0
        m_des = 0
        f_des = 0

        for eu in leu:
            sel = 0
            des = 0
            li_rcvd = [0,0,0,0] # no, mn, my, yes
            li_gave = [0,0,0,0] # no, mn, my, yes
            
            for ix in [ixobj for ixobj in li_r1_ix_analyzed if eu.eu_num in 
            [ixobj.m_eu_num, ixobj.f_eu_num]]:
                if eu.eu_num == ix.m_eu_num: # male or male ghost
                    sel += ix.m_sac
                    des += ix.f_sac
                    li_gave[ix.m_sac] += 1
                    li_rcvd[ix.f_sac] += 1
                    
                else: # female or female ghost
                    sel += ix.f_sac
                    des += ix.m_sac
                    li_gave[ix.f_sac] += 1
                    li_rcvd[ix.m_sac] += 1
                    

            eu.r1_sel = sel
            eu.r1_des = des

            eu.nr1g_no = li_gave[0]
            eu.nr1g_mn = li_gave[1]
            eu.nr1g_my = li_gave[2]
            eu.nr1g_yes = li_gave[3]

            eu.nr1r_no = li_rcvd[0]
            eu.nr1r_mn = li_rcvd[1]
            eu.nr1r_my = li_rcvd[2]
            eu.nr1r_yes = li_rcvd[3]

            eu.nr1g_total = li_gave[0] + 2*li_gave[1] + 3*li_gave[2] + 4*li_gave[3] # should = sel
            eu.nr1r_total = li_rcvd[0] + 2*li_rcvd[1] + 3*li_rcvd[2] + 4*li_rcvd[3] # should = des

        # go back into ix's and put in r1_m_des, r1_m_sel, r1_f_des, r1_f_sel, r1_likeness, etc.
        li_qa_count_by_eu = [0]*self.e.num_all_eu
        for ix in li_r1_ix_analyzed:
            li_qa_count_by_eu[ix.m_eu_num-1] += 1
            li_qa_count_by_eu[ix.f_eu_num-1] += 1
            for eu in leu:
                if eu.eu_num == ix.m_eu_num:
                    ix.r1_m_des = eu.r1_des
                    ix.r1_m_sel = eu.r1_sel
                elif eu.eu_num == ix.f_eu_num:
                    ix.r1_f_des = eu.r1_des
                    ix.r1_f_sel = eu.r1_sel
            ix.r1_likeness = ( # closer to 0 is better
                abs((ix.r1_m_des) - (ix.r1_f_des)) 
              + abs((ix.r1_m_sel) - (ix.r1_f_sel))
                 ) * (-1)

        # Sort list according to energy descending.
        # Energy is a loose term for how much the ix deserves to happen again.
        li_r1_ix_analyzed = sorted(
            [ix for ix in li_r1_ix_analyzed if (
             ix.meu.sex != 'MG' and ix.feu.sex != "FG")], key = lambda i: [
                
                # Best SAC pair
                # (3,3)>(3,2)>(2,2)>(3,1)>(2,1)>(1,1)>(3,0)>(2,0)>(1,0)>(0,0)
                i.sac_total - abs(i.m_sac - i.f_sac), # (6)>(4)>(4)>(3)>(2)>(2)>(0)>(0)>(0)>(0)
                i.sac_total, # makes (3,2)>(2,2); makes (2,1)>(1,1); makes (3,0)>(2,0)>(1,0)>(0,0)

                # most similar in desirability and selectivity in round
                # (lowest sum of differences in them)
                i.r1_likeness, 

                i.r1_m_sel + i.r1_f_sel, # most selective pair of round
                #i.m_nixness + i.f_nixness, # most selective pregame pair
                i.r1_m_des + i.r1_f_des, # most desirable pair of round
                #i.m_hotness + i.f_hotness # most desirable pregame pair

                # most similar qa counts
                (-1)*abs(li_qa_count_by_eu[i.m_eu_num-1] - li_qa_count_by_eu[i.f_eu_num-1])

            ],
            reverse = True)     

        # add r1_rank to all ix's
        for index, ix in enumerate(li_r1_ix_analyzed):
            ix.r1_rank = index + 1


        return li_r1_ix_analyzed


    pass

###############################################################################
"""                               Round 2                                   """
###############################################################################

class Round_2(_Round):

    def __init__(self, e):
        _Round.__init__(self, e)
        self.e = e
        self.round_num = 2
        self.num_ix_pp = self.e.num_r2_ix_pp
        pass



    def simulate(self, lix):
        """
        Pretty much copied from Round_1.simulate -- can I somehow combine them?

        Also, I'm confused about whether lists that get passed as arguments are
        updated, or whether I need to create copies, or whether I need to create
        copy.deepcopies, or whether I should keep a copy of each kind of ix list
        ...but I can figure that stuff out later. As long as what I have works.
        """
        #self.lix = lix

        li_r2_ix_simulated = lix # though it's not simulated yet

        for ix in li_r2_ix_simulated:

            ix.m_sac = random.randint(0,3)
            ix.f_sac = random.randint(0,3)
            ix.m_qa = random.choice(['A','B','C','D'])
            ix.f_qa = random.choice(['A','B','C','D'])

            ix.sac_total = ix.m_sac + ix.f_sac
            ix.sac_same = 1 if ix.m_sac == ix.f_sac else 0
            ix.qa_same = 1 if ix.m_qa == ix.f_qa else 0

        return li_r2_ix_simulated # necessary?   



    def analyze(self, leu, lix):

        li_r2_ix_analyzed = lix

        m_sel = 0
        f_sel = 0
        m_des = 0
        f_des = 0

        for eu in leu: # 51x
            sel = 0
            des = 0
            li_rcvd = [0,0,0,0] # no, mn, my, yes
            li_gave = [0,0,0,0] # yes, my, mn, no
            # for ix in li_r2_ix_analyzed: # 2601x
            for ix in [ixobj for ixobj in li_r2_ix_analyzed
                if eu.eu_num in [ixobj.m_eu_num, ixobj.f_eu_num]
                ]: # 2601x
                if eu.eu_num == ix.m_eu_num: # male or male ghost
                    sel += ix.m_sac
                    des += ix.f_sac
                    li_gave[ix.m_sac] += 1
                    li_rcvd[ix.f_sac] += 1
                    
                else: # female or female ghost
                    sel += ix.f_sac
                    des += ix.m_sac
                    li_gave[ix.f_sac] += 1
                    li_rcvd[ix.m_sac] += 1
                    

            eu.r2_sel = sel
            eu.r2_des = des

            eu.nr2g_no = li_gave[3]
            eu.nr2g_mn = li_gave[2]
            eu.nr2g_my = li_gave[1]
            eu.nr2g_yes = li_gave[0]

            eu.nr2r_no = li_rcvd[0]
            eu.nr2r_mn = li_rcvd[1]
            eu.nr2r_my = li_rcvd[2]
            eu.nr2r_yes = li_rcvd[3]

            eu.nr2g_total = li_gave[0] + 2*li_gave[1] + 3*li_gave[2] + 4*li_gave[3] # should = sel
            eu.nr2r_total = li_rcvd[0] + 2*li_rcvd[1] + 3*li_rcvd[2] + 4*li_rcvd[3] # should = des

        # go back into ix's and put in r2_m_des, r2_m_sel, r2_f_des, r2_f_sel, r2_likeness
        # (tiebreaker for determining energy)
        for ix in li_r2_ix_analyzed:
            for eu in leu:
                if eu.eu_num == ix.m_eu_num:
                    ix.r2_m_des = eu.r2_des
                    ix.r2_m_sel = eu.r2_sel
                elif eu.eu_num == ix.f_eu_num:
                    ix.r2_f_des = eu.r2_des
                    ix.r2_f_sel = eu.r2_sel
            ix.r2_likeness = ( # closer to 0 is better
                abs((ix.r2_m_des+ix.m_hotness) - (ix.r2_f_des+ix.f_hotness)) 
              + abs((ix.r2_m_sel+ix.m_nixness) - (ix.r2_f_sel+ix.f_nixness))
                 ) * (-1)

        # Sort list according to energy descending.
        # Energy is a loose term for how much the ix deserves to happen again.
        li_r2_ix_analyzed = sorted(
            [ix for ix in li_r2_ix_analyzed if (
                ix.meu.sex != 'MG' and ix.feu.sex != "FG")], key = lambda i: [
                 # (3,3)>(3,2)>(2,2)>(3,1)>(2,1)>(1,1)>(3,0)>(2,0)>(1,0)>(0,0)

                     i.sac_total - abs(i.m_sac - i.f_sac), # (6)>(4)>(4)>(3)>(2)>(2)>(0)>(0)>(0)>(0)
                     i.sac_total, # makes (3,2)>(2,2); makes (2,1)>(1,1); makes (3,0)>(2,0)>(1,0)>(0,0)

                     i.r2_likeness, # most similar in desirability and selectivity
                                    # (have lowest differences in them)

                     i.r2_m_sel + i.r2_f_sel, # most selective pair of round
                     i.m_nixness + i.f_nixness, # most selective pregame pair
                     i.r2_m_des + i.r2_f_des, # most desirable pair of round
                     i.m_hotness + i.f_hotness # most desirable pregame pair

            ],
            reverse = True)     

        # add r2_rank to all ix's
        for index, ix in enumerate(li_r2_ix_analyzed):
            ix.r2_rank = index + 1

        return li_r2_ix_analyzed      


    pass

###############################################################################
"""                               Round 3                                   """
###############################################################################

class Round_3(_Round):

    def __init__(self, e):
        _Round.__init__(self, e)
        self.round_num = 3
        self.num_ix_pp = self.e.num_r3_ix_pp
        pass

    def simulate(self, lix):
        return lix

    def analyze(self, leu, lix):
        return lix

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

    TOTAL_IX_NUM = 0
    CURR_IX_NUM = 0 # will be reset after each round

    def __init__(self, e, r, mEU, fEU):
        _Interaction.TOTAL_IX_NUM += 1
        _Interaction.CURR_IX_NUM += 1
        self.e = e
        self.r = r
        self.meu = mEU
        self.feu = fEU

        self.ix_num = _Interaction.CURR_IX_NUM
        self.event_num = self.e.event_num
        self.round_num = self.r.round_num

        self.m_eu_num = self.meu.eu_num
        self.f_eu_num = self.feu.eu_num

        self.m_sex = mEU.sex
        self.f_sex = fEU.sex

        self.will_sa = 0

    # def simulate(self):
    #     self.m_see_f = random.randint(0, 3)
    #     self.f_see_m = random.randint(0, 3)
    #     # self.m_see_f = random.choice(["no", "maybe-no", "maybe-yes", "yes"])
    #     # self.f_see_m = random.choice(["no", "maybe-no", "maybe-yes", "yes"])
    #     pass

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

    #CURR_USER_NUM = 0

    def __init__(self, gender):

        _User.CURR_USER_NUM += 1
        self.u_num = _User.CURR_USER_NUM

        self.sex = gender

        self.full_name = self.make_name()

        self.hotness = random.randint(5, 95)
        self.nixness = random.randint(max(self.hotness-30, 5), 
                                      min(self.hotness+30, 95))
        self.personality = random.randint(5, 95)
        self.age = random.randint(18, 22)
        self.eyes = random.choice(["blue", "brown", "black", "green", "hazel"])

        pass

    def make_name(self):
        if self.sex in ['M','MG']:
            full_name = names.get_full_name(gender = "male")
        else:
            full_name = names.get_full_name(gender = "female")

        print(self.u_num, full_name, self.sex)        
        return full_name

    def __iter__(self):
        # first start by grabbing the Class items
        iters = dict((x,y) for x,y in _User.__dict__.items() 
            if x[:2] != '__' 
                and x != "simulate"
                and x != "make_name"
                and x != "CURR_USER_NUM"
            )
        # then update the class items with the instance items
        iters.update(self.__dict__)
        # now 'yield' through the items
        for x,y in iters.items():
            yield x,y

    # def __repr__(self):
    #     return "{} {}".format(self.__class__.__name__, self.u_num)

    
    pass

################################################################################
"""                                _EVENTUSER                                 """
################################################################################

class _EventUser(_User):

    CURR_EVENTUSER_NUM = 0

    def __init__(self, e, u):
        _EventUser.CURR_EVENTUSER_NUM += 1
        self.eu_num = _EventUser.CURR_EVENTUSER_NUM
        self.u_num = u.u_num
        self.sex = u.sex
        self.full_name = u.full_name
        self.first_name = self.full_name.split(" ")[0]
        self.last_name = self.full_name.split(" ")[-1]
        self.hotness = u.hotness
        self.nixness = u.nixness
        self.personality = u.personality
        self.age = u.age
        self.eyes = u.eyes
        pass

    def __iter__(self):
        # first start by grabbing the Class items
        iters = dict((x,y) for x,y in _EventUser.__dict__.items() 
            if x[:2] != '__' 
                and x != "CURR_EVENTUSER_NUM"
            )
        # then update the class items with the instance items
        iters.update(self.__dict__)
        # now 'yield' through the items
        for x,y in iters.items():
            yield x,y

    pass
################################################################################
"""                                  _IPAD                                   """
################################################################################

################################################################################
"""                                _QUESTION                                 """
################################################################################

################################################################################
"""                          LI_ORDERED_ATTR_NAMES                           """
################################################################################

def li_ordered_attr_names(obj):
    """  
    Returns an ordered list of attribute names for each class (each tab in Excel).
    Useful for ignoring class instances (objects) when writing to Excel,
    and for making sure everything stays in a familiar order when testing.
    """
    li_names = []
    li_keys = dict(obj).keys()
    #print("\n", type(obj).__name__, "\nUnsorted:", li_keys)

    for name in [

                "e_num", "r_num", # for all classes?
                "sub_num", "sta_num", "ix_num", # for Interactions

                "m_eu_num", "f_eu_num", # for Interactions
                "u_num", "eu_num", # for Users and EventUsers

                "first_name", "last_name", "full_name", # for Users and Event Users
                
                "m_sac", "f_sac", "sac_total", "sac_same", # for Interactions
                "r1msac", "r1fsac", 
                "r2msac", "r2fsac",
                "r3msac", "r3fsac",


                "m_qa", "f_qa", "qa_same", "q_num", # for Interactions

                "r1_sac_tot", "r2_sac_tot", "r3_sac_tot", # for Ix in R2 and R3
                                
                "hotness", "nixness", "personality", # for all classes
                "sex", "age", "height", "eyes", "experience", # for all classes

                "m_hotness", "m_nixness", "m_personality", # for all classes
                "m_sex", "m_age", "m_height", "m_eyes", "m_experience", # for all classes

                "f_hotness", "f_nixness", "f_personality", # for all classes
                "f_sex", "f_age", "f_height", "f_eyes", "f_experience", # for all classes

                "r1_sel", "r2_sel", "r3_sel", # for EventUsers
                "r1_des", "r2_des", "r3_des", # for EventUsers

                "r1_m_sel", "r2_m_sel", "r3_m_sel", # for Interactions
                "r1_m_des", "r2_m_des", "r3_m_des", # for Interactions
                "r1_f_sel", "r2_f_sel", "r3_f_sel", # for Interactions
                "r1_f_des", "r2_f_des", "r3_f_des", # for Interactions

                "nr1r_yes", "nr1r_my", "nr1r_mn", "nr1r_no", # for EventUsers
                "nr1g_yes", "nr1g_my", "nr1g_mn", "nr1g_no", # for EventUsers
                "nr2r_yes", "nr2r_my", "nr2r_mn", "nr2r_no", # for EventUsers
                "nr2g_yes", "nr2g_my", "nr2g_mn", "nr2g_no", # for EventUsers
                "nr3r_yes", "nr3r_my", "nr3r_mn", "nr3r_no", # for EventUsers
                "nr3g_yes", "nr3g_my", "nr3g_mn", "nr3g_no", # for EventUsers

                "r1_likeness", "r2_likeness", "r3_likeness", # for Interactions
                "r1_rank", "r2_rank", "r3_rank", # for Interactions
                "will_sa", # for Interactions

                "m_ipad_num", "f_ipad_num", # for Interactions
                "m_next_ix_ipad_num", "f_next_ix_ipad_num" # for Interactions

                ]:
        if name in li_keys:
            li_names.append([key for key in li_keys if key == name][0])
    #print("Sorted:", li_names)

    return li_names


################################################################################
"""                 CREATE_QA_AND_SAC_DATABASES_IN_FIREBASE                  """
################################################################################

def create_QA_and_SAC_databases_in_Firebase(e, leu, flat = True):
    """
    Sets up an empty database in Firebase with 3 main nodes: IX, SAC and QA.

    Firebase seems to be able to create or update about 11-12 records / second,
    = 700 / minute, so keep that in mind when creating this database. Try to
    minimize how much data needs to be (temporarily) stored in Firebase during
    an event.

    These DB nodes have different functions:

    "Event" -> "0000" -> "Round" -> "1" -> "EventUser" -> "001" -> "first_name" : eu.first_name
    "Event" -> "0000" -> "Round" -> "1" -> "EventUser" -> "001" -> "SAC" -> "no" : 0
    "Event" -> "0000" -> "Round" -> "1" -> "EventUser" -> "001" -> "SAC" -> "yes": 0

    "zE0000R1" -> "EventUser_001" -> "first_name" : eu.first_name
    "zE0000R1" -> "EventUser_001" -> "SAC_yes" : nr1g_yes
    "zE0000R1_EventUser_001" -> "SAC_yes" : nr1g_yes
    zE0000 -> r1sac -> eu_num_001 -> nr1g_yes
    -- Realtime on-screen SAC-so-far counts that people see during ix's.
    -- iPads upload to this during events; data is transported into Parse later.


    """

    ref_root = Firebase('https://burning-fire-8681.firebaseio.com')

    ref_Event = ref_root.child("Event_{}{}".format())

    hasData = ref_Event.child("hasData").get()

    if hasData in [True, "True", "true"]:
        print ("Firebase structure already exists")
        return
    elif hasData in [False, "False", "false"]:
        print ("Starting from an empty Firebase")

    db1_start_time = time.time()

    if flat == True:

        # 3 x 102 x 5 = 1,530 records, takes about 110 seconds
        for round_num in [1]: # for each round (x3)
            ref_round = ref_Event.child("Round {}".format(str(round_num)))
            for index, eu in enumerate(leu[:15]): # for each event user (x102)
                ref_EU = ref_round.child("EventUser_{}{}".format(
                    "0"*(3-len(str(eu.eu_num))), 
                    str(eu.eu_num))
                    )
                ref_EU.put({ # (x5)
                    "first_name": eu.first_name,
                    "eu_num": eu.eu_num,
                    "SAC_yes": 0,
                    "SAC_my": 0,
                    "SAC_mn": 0,
                    "SAC_no": 0
                    })
            # for q_num in e.li_q_nums:
            #     ref_QA = ref_round.child("Question_{}{}".format(
            #         "0"*(3-len(str(q_num))),
            #         str(q_num)
            #         ))

        ref_Question = ref_Event.child("Question")
        for q_num in e.li_q_nums:
            ref_q = ref_Question.child("q_num_{}{}".format("0"*(3-len(str(q_num))), str(q_num)))
            ref_q.put( {
                "q_text": "___, ___, jingle all the way.",
                "q_answers": {
                    "1": None,
                    "2": None
                    }
                })

                #ref_EU.post({ # equivalent to "push()" in Firebase; creates unique id's for each node



    else:
        for rd_num in [1]:
            ref_e = ref_Event.child(e.event_serial)
            ref_Round = ref_e.child("Round")
            ref_r = ref_Round.child(str(rd_num))
            ref_EventUser = ref_r.child("EventUser")
            for eu in leu[:10]:
                ref_eu = ref_EventUser.child("{}{}".format("0"*(3-len(str(eu.eu_num))), str(eu.eu_num)))
                ref_eu.put(
                    {
                        "first_name": eu.first_name,
                        "SAC": {
                                "yes": 0,
                                "my": 0,
                                "mn": 0,
                                "no": 0
                                }    
                    })



    db1_stop_time = time.time()
    print("DB 1 took {} seconds to create.".format(
        round(db1_stop_time - db1_start_time, 2)))
    db2_start_time = time.time()


    # 1 x 102 = 102 records, takes about ________ seconds



    db2_stop_time = time.time()
    print("DB 2 took {} seconds to create.".format(
        round(db2_stop_time - db2_start_time, 2)))

            # ref_ix = ref_ip_num.child("IX")
            # ref_sac_yes = ref_ip_num.child("ix{}{}".format("0"*(4-len())))
    pass


################################################################################
"""                     GET_PERFECT_MAXIMUM_MATCHINGS                        """
################################################################################

def get_perfect_maximum_matchings(e, r, leu, lix):

    # Split the list of eu's by gender.
    # Are these new lists, or do they still update e.li_all_eu?
    li_all_meu = [eu for eu in leu if eu.sex in ['M', 'MG']]
    li_all_feu = [eu for eu in leu if eu.sex in ['F', 'FG']]

    # # Make a deepcopy of lix so as not to change the passed-in list.
    # li = copy.deepcopy(lix)
    
    # # Create lists of ix's by SAC pair (excluding the ix's with any 0).
    # li_33 = [ix for ix in li if ix.sac_total == 6]
    # li_32 = [ix for ix in li if ix.sac_total == 5]
    # li_22 = [ix for ix in li if ix.m_sac == 2 and ix.f_sac == 2]
    # li_31 = [ix for ix in li if (ix.m_sac == 3 and ix.f_sac == 1) or (
    #                              ix.m_sac == 1 and ix.f_sac == 3)]
    # li_21 = [ix for ix in li if (ix.m_sac == 2 and ix.f_sac == 1) or (
    #                              ix.m_sac == 1 and ix.f_sac == 2)]
    # li_11 = [ix for ix in li if ix.m_sac == 1 and ix.f_sac == 1]
    # li_30 = [ix for ix in li if (ix.m_sac == 3 and ix.f_sac == 0) or
    #                             (ix.m_sac == 0 and ix.f_sac == 3)]

    li_no_0 = [ix for ix in lix if ix.m_sac != 0 and ix.f_sac != 0]
    li_no_00 = [ix for ix in lix if not (ix.m_sac == 0 and ix.f_sac == 0)]

    # Make matrices of slots representing ix 'appointments'.
    # Row is subround-1; Column is eu_num-1; value is sta_num.
    # array([[ 0,  0,  0,  ...,  0],
           # [ 0,  0,  0,  ...,  0],
           # ...                   ,
           # [ 0,  0,  0,  ...,  0]])
    li_m_slots = numpy.zeros((r.num_ix_pp, len(li_all_meu)), dtype = int)
    li_f_slots = numpy.zeros((r.num_ix_pp, len(li_all_feu)), dtype = int)

    ld_m_sta_num_by_sub = [{} for i in range(r.num_ix_pp)]
    ld_f_sta_num_by_sub = [{} for i in range(r.num_ix_pp)]

    for subround in range(r.num_ix_pp):
        for index, feu in enumerate(li_all_feu):
            ld_f_sta_num_by_sub[subround][str(feu.eu_num)] = index + 1
        # rotate list -- first feu moved to back of list
        li_all_feu = li_all_feu[1:] + [li_all_feu[0]]        

    # # Put the women in their stations for all subrounds.
    # # They start at a station 51 less than their eu num, and they move 
    # # right (counter-clockwise) by 1 from outer circle (-1) after each ix
    # for subround in range(r.num_ix_pp):
    #     for index, feu in enumerate(li_all_feu):
    #         #li_f_slots[subround][index] = feu.eu_num
    #         li_f_slots[subround][feu.eu_num-1] = index + 1
    #     # rotate list -- first feu moved to back of list
    #     li_all_feu = li_all_feu[1:] + [li_all_feu[0]]

    # Make a list of sets of eu_num's who have an ix in a subround (index of list).
    liset_eunum_with_ix_by_subround = [set([]) for x in range(r.num_ix_pp+1)]

    # Initilize the list of planned/scheduled ix's we're gonna return.
    li_ix_planned = []


    # START "MAXIMUM BIPARTITE MATCHING" ALGORITHM

    # make the inital graphs
    graph_no_0 = list((ix.m_eu_num, ix.f_eu_num, (-1)*(index+1)) for index, ix in enumerate(li_no_0))
    graph_no_00 = list((ix.m_eu_num, ix.f_eu_num, (-1)*(index+1)) for index, ix in enumerate(li_no_00))
    graph_copy = copy.deepcopy(graph_no_00) # This is so we don't lose the original ranks of the ix's.


    # # make list of subround sums of ranks
    # li_sums_ranks = []

    # make a list of lists of tuples we get from mwm. Each list is a subround.
    lilitu_repr_an_ix = [list([]) for x in range(r.num_ix_pp)]

    # For each subround, make a perfect mwm, add it to 
    # the lilitu_repr_an_ix, and remove it from the graph.
    for subround in range(r.num_ix_pp):

        # Make a list to hold the mwm's tuples for this subround.
        litu_subround = []

        # Find a maximum weighted matching representing the subround's ix
        # assignments.
        mwm = maxWeightMatching(graph_no_00, maxcardinality = True)[1:]
        
        if mwm.count(-1) == 0:
            print("(Perfect matching for Round {}, subround {}!)".format(r.round_num, subround+1))
        else:
            print("{} eu's weren't matched for subround {}.".format(mwm.count(-1), subround+1))
            return

        # Make a list of 3-tuples representing the mwm: (m_eu_num, f_eu_num, station).
        # Just going through half of the list is enough.
        litu_subround = list((index+1, n) for index, n in enumerate(mwm[:e.num_m_eu_p]))

        # Add the guy's eunum to the male ld of station numbers.
        for (guy_eunum, girl_eunum) in litu_subround:
            ld_m_sta_num_by_sub[subround][str(guy_eunum)] = ld_f_sta_num_by_sub[subround][str(girl_eunum)]

        # # Add the guy's eunum to the male ld of station numbers.
        # for subr, li_slots_in_subround in enumerate(list(li_m_slots)):
            
        # for index, slot in enumerate(list(li_m_slots[subround])):

        #     li_m_slots[subr][li_m_slots[subr].index()]


        # # Make a list of ranks for the subround, and add its sum to a list
        # # of sums by subround.
        # li_ranks = []
        # for tu in litu_subround: # ()
        #     for tu_edge in graph_no_00: # (meunum, feunum, -1 * rank)
        #         if tu_edge[0] == tu[0] and tu_edge[1] == tu[1]:
        #             li_ranks.append((-1)*tu_edge[2])
        # li_ranks.sort()
        # li_sums_ranks.append(sum(li_ranks))

        # Remove the edges of the mwm from the graph copy.
        for index, tu_edge in enumerate(graph_copy):
            m_eu_num = tu_edge[0]
            f_eu_num = tu_edge[1]
            rank = tu_edge[2]
            if (m_eu_num, f_eu_num) in litu_subround:
                lilitu_repr_an_ix[subround].append(tu_edge)
                graph_no_00.remove(tu_edge)



    # Now that we're done, print a list of the ranks that didn't happen 
    # again, plus some other info about the round.
    ###li_ranks_dn_happen = sorted([(-1) * tu_edge[2] for tu_edge in graph_no_00])
    ###print("\n\nli_ranks_didnt_happen:\n{}\n".format(li_ranks_dn_happen))
    ###print("li_sums_ranks:\n{}\n".format(li_sums_ranks))
    ###print("Total sum of ranks: {}\n".format(sum(li_sums_ranks)))
    ###print("Average rank: {}\n".format(round(sum(li_sums_ranks)/(e.num_m_eu_p*nr3g_.num_ix_pp), 2)))


    # Make sure the guy is moving at least 5 stations away btwn ix's.
    pprint(ld_m_sta_num_by_sub)
    pprint(ld_f_sta_num_by_sub)

    for i in range(10):
        if not guys_are_walking(ld_m_sta_num_by_sub, min_distance = 5):
            # Rearrange the subround ld's for ...
            pass




    # Make the new ix's and put them in a list to return.
    for s_index, subround_li in enumerate(lilitu_repr_an_ix):
        for t_index, tu in enumerate(subround_li):

            # Make an interaction from the tuple.
            m = tu[0] # m_eu_num
            f = tu[1] # f_eu_num
            rank = (-1)*tu[2] # rank
            meu = leu[m-1]
            feu = leu[f-1]
            newix = _Interaction(e, r, meu, feu) # Make new ix object.
            newix.sub_num = s_index + 1
            newix.sta_num = ld_f_sta_num_by_sub[s_index][str(f)]
            #newix.sta_num = list(li_f_slots[s_index]).index(f) + 1
            #li_m_slots[s_index][]
            newix.m_ipad_num = e.li_m_ipad_nums[newix.sta_num-1]
            newix.f_ipad_num = e.li_f_ipad_nums[newix.sta_num-1]
            newix.m_hotness = meu.hotness
            newix.f_hotness = feu.hotness
            newix.m_nixness = meu.nixness
            newix.f_nixness = feu.nixness
            newix.m_personality = meu.personality
            newix.f_personality = feu.personality
            newix.r1_likeness = ix.r1_likeness
            newix.r1_rank = ix.r1_rank
            newix.r1_m_sel = ix.r1_m_sel # or, meu.r1_sel
            newix.r1_f_sel = ix.r1_f_sel
            newix.r1_m_des = ix.r1_m_des
            newix.r1_f_des = ix.r1_f_des
            newix.r1msac = ix.m_sac
            newix.r1fsac = ix.f_sac   
            newix.r1_sac_tot = ix.sac_total        
            li_ix_planned.append(newix)

    return li_ix_planned



################################################################################
################################################################################
################################################################################
###                                                                          ###
"""                                  MAIN                                    """
###                                                                          ###
################################################################################
################################################################################
################################################################################

def simulate_daeious_event():
    """
    1. Create fake users, ghosts, ipads, questions from helper functions
    5. Create and simulate an event by calling simulate()
    7. Run tests on results.
    """

    start = time.time()

    """  Create 1 _Event object.
    """
    e = _Event(
        EVENT_NUMBER = 0,
        MEN = 51,
        WOMEN = 51,
        START_AT_ROUND = 0,
        SEC_PER_R1_IX = 20,
        SEC_PER_R2_IX = 40,
        SEC_PER_R3_IX = 60
        )


    """  Optimize event timing.  
    """

    """  Create a bunch of Users.
    """
    _User.CURR_USER_NUM = 0
    li_mpu = list((_User('M') for i in range(int(1.0*e.num_m_eu_p))))
    li_fpu = list((_User('F') for i in range(int(1.0*e.num_f_eu_p))))
    li_mgu = list((_User('MG') for i in range(5*e.num_m_eu_g)))
    li_fgu = list((_User('FG') for i in range(5*e.num_f_eu_g)))
    li_all_u = li_mpu + li_fpu + li_mgu + li_fgu
    # reset CURR_USER_NUM
    _User.CURR_USER_NUM = 0


    """  Create correct number and type of EventUsers.  
    """
    li_mpeu = list((_EventUser(e, u) for u in li_mpu[:e.num_m_eu_p]))
    li_fpeu = list((_EventUser(e, u) for u in li_fpu[:e.num_f_eu_p]))
    li_mgeu = list((_EventUser(e, u) for u in li_mgu[:e.num_m_eu_g]))
    li_fgeu = list((_EventUser(e, u) for u in li_fgu[:e.num_f_eu_g]))
    li_all_eu = li_mpeu + li_fpeu + li_mgeu + li_fgeu
    # reset CURR_EVENTUSER_NUM
    _EventUser.CURR_EVENTUSER_NUM = 0


    """  Create up to 5 _Round objects.  
    """
    r0 = Round_0(e) if e.start_at_round <= 0 else 0
    r1 = Round_1(e) if e.start_at_round <= 1 else 0
    r2 = Round_2(e) if e.start_at_round <= 2 else 0
    r3 = Round_3(e) if e.start_at_round <= 3 else 0
    r4 = Round_4(e) if e.start_at_round <= 4 else 0


    """ Create a skeleton DB in Firebase for the simulated event.
    """
    create_QA_and_SAC_databases_in_Firebase(e, li_all_eu, flat = True)


    """  Plan, simulate, and analyze the rounds.  
    """


    """  ROUND 1  """
    li_r1_ix_planned = r1.plan(leu = li_all_eu)
    li_r1_ix_simulated = r1.simulate(lix = li_r1_ix_planned)
    li_r1_ix_analyzed = r1.analyze(leu = li_all_eu, lix = li_r1_ix_simulated)
    _Interaction.CURR_IX_NUM = 0


    """  ROUND 2  """
    li_r2_ix_planned = r2.plan_A(leu = li_all_eu, lix = li_r1_ix_analyzed)
    li_r2_ix_simulated = r2.simulate(li_r2_ix_planned)
    li_r2_ix_analyzed = r2.analyze(leu = li_all_eu, lix = li_r2_ix_simulated)
    # reset _Interaction.CURR_IX_NUM
    _Interaction.CURR_IX_NUM = 0

    """  ROUND 3  """
    li_r3_ix_planned = r3.plan_A(leu = li_all_eu, lix = li_r2_ix_analyzed)
    li_r3_ix_simulated = r3.simulate(li_r3_ix_planned)
    li_r3_ix_analyzed = r3.analyze(leu = li_all_eu, lix = li_r3_ix_simulated)
    # reset _Interaction.CURR_IX_NUM
    _Interaction.CURR_IX_NUM = 0


    """  Set most "full" / up-to-date round interaction lists for Excel writing
    """
    li_r1_ix = li_r1_ix_analyzed
    li_r2_ix = li_r2_ix_analyzed
    li_r3_ix = li_r3_ix_analyzed


    """  Create all sheets in Excel.
    """
    WB = excel.Workbook()

    ws_User = WB.add_sheet('Users', cell_overwrite_ok = True)
    ws_EventUser = WB.add_sheet('Event Users', cell_overwrite_ok = True)
    ws_r1_ix = WB.add_sheet('R1 Ix', cell_overwrite_ok = True)
    ws_r2_ix = WB.add_sheet('R2 Ix', cell_overwrite_ok = True)
    ws_r3_ix = WB.add_sheet('R3 Ix', cell_overwrite_ok = True)

        #  Users
    """  Write the rows of Users in Excel  """
    print("Writing Users to Excel")
    for c, label in enumerate(li_ordered_attr_names(li_all_u[0])):
        ws_User.write(0, c, label)
        for r, user in enumerate(li_all_u):
            ws_User.write(r+1, c, getattr(user, label))   

        #  Event Users
    """  Write the rows of EventUsers in Excel  """
    print("Writing EventUsers to Excel")
    for c, label in enumerate(li_ordered_attr_names(li_all_eu[0])): # for each attribute
        ws_EventUser.write(0, c, label) # make the column label in the first row
        for r, event_user in enumerate(li_all_eu): # for each EventUser
            ws_EventUser.write(r+1, c, getattr(event_user, label))

        #  Interactions
    """  Write the rows of Interactions in Excel  """
    print("Writing Interactions to Excel")
    for sheet, li in zip([ws_r1_ix, ws_r2_ix, ws_r3_ix], [li_r1_ix, li_r2_ix, li_r3_ix]): # for each round
        print("Writing Round")
        for c, label in enumerate(li_ordered_attr_names(li[0])): # for each column / attribute of an interaction
            sheet.write(0, c, label) # make the column label in the first row
            for r, ix in enumerate(li):
                sheet.write(r+1, c, getattr(ix, label))

    WB.save('example.xls')    


    # Run tests on the results.

    end = time.time()

    return round(end-start, 2)


def main():
    li_info = []
    for i in range(1):
        li_info.append(simulate_daeious_event())
    pass


if __name__ == '__main__':
    logging.getLogger('backoff').addHandler(logging.StreamHandler())
    start = time.time()
    status = main()
    print("\n---\n\ndaeious.py has finished running in {} seconds.\n".format(
        round(time.time() - start, 2)))
    sys.exit(status)































