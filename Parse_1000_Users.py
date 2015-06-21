""" Create 1000 fake User objects in Parse.
"""

# import stuff
import math
import random
import sys
import time
import json, httplib
from pprint import pprint

import names # https://github.com/treyhunner/names

# Import ParsePy stuff. ParsePy makes using Parse in Python much easier.
from parse_rest.connection import ParseBatcher, register, SessionToken
from parse_rest.datatypes import ACL, Function, Object
from parse_rest.role import Role
from parse_rest.user import User

# Calling "register" allows parse_rest / ParsePy to work.
# - register(APPLICATION_ID, REST_API_KEY, optional MASTER_KEY)
register("AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", 
     "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS", 
     master_key = "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv"
  )

class _User(object):

    CURR_U_NUM = 0

    def __init__(self):
        _User.CURR_U_NUM += 1
        self.u_num = _User.CURR_U_NUM
        self.un_str = self.make_serial()
        self.sex = random.choice(['M', 'F'])
        self.age = random.randint(18, 24)
        self.dob = self.make_dob()
        self.eyes = random.choice(["blue", "brown", "black", "green", "hazel"])
        self.full_name = self.make_name()
        self.first_name = self.full_name.split(' ')[0]
        self.last_name = self.full_name.split(' ')[-1]
        self.college = random.choice(["Harvard", "MIT", "UNH", "Centre", "Exeter"])
        self.email_address = self.last_name + "." + self.first_name + "@gmail.com"
        self.username = self.first_name.lower()[0] + self.last_name.lower() + str(random.randint(1, 999))
        self.li_events_registered = []

    def make_name(self):
        if self.sex == 'M':
            return names.get_full_name(gender = "male")
        else:
            return names.get_full_name(gender = "female")

    def make_serial(self):
        return "{}{}".format("0"*(5 - len(str(self.u_num))), self.u_num)

    def make_dob(self):
        birth_year = 2015 - self.age
        birth_month = random.randint(1, 12)
        if birth_month in (1,3,5,7,8,10,12):
            birth_day = random.randint(1, 31)
        elif birth_month in (9,4,6,11):
            birth_day = random.randint(1, 30)
        else: # February
            birth_day = random.randint(1, 28)
        return str(birth_month) + "/" + str(birth_day) + "/" + str(birth_year)

    def __iter__(self):
        # first start by grabbing the Class items
        iters = dict((x,y) for x,y in _User.__dict__.items() 
            if x[:2] != '__' 
                and x != "CURR_U_NUM"
                and x != "make_name"
                and x != "make_serial"
                and x != "make_dob"
            )
        # then update the class items with the instance items
        iters.update(self.__dict__)
        # now 'yield' through the items
        for x,y in iters.items():
            yield x,y

    pass



def register_for_events(li_u):

    # n = number of people of each sex at a full event
    n = 51

    # make temp lists of male users and female users
    li_mu = [u for u in li_u if u.sex == 'M']
    li_fu = [u for u in li_u if u.sex == 'F']

    # give out spots for 20 full events (1020 spots for each sex)
    # some will go to several events, some will go to none - completely random
    for e_num in range(20): # for each of 20 events:
        mu_sample = random.sample(li_mu, n) # pick n males to register
        fu_sample = random.sample(li_fu, n) # pick n females to register
        for spot in range(n):
            # add e_num to their list of events for which they're registered
            mu_sample[spot].li_events_registered.append(e_num+1)
            fu_sample[spot].li_events_registered.append(e_num+1)

    pass


def create_1000_users_in_Parse():

    li_u = []

    for i in range(1000):
        u = _User()
        li_u.append(u)

    register_for_events(li_u)

    for u in li_u:

        User.signup( username = u.username, password = "1234", 
            u_num = u.u_num,
            sex = u.sex,
            age = u.age,
            eyes = u.eyes,
            dob = u.dob,
            full_name = u.full_name,
            first_name = u.first_name,
            last_name = u.last_name,
            college = u.college,
            email_address = u.email_address,
            li_events_registered = u.li_events_registered)

        print "User {} signed up.".format(u.u_num)


    # batcher = ParseBatcher()
    # batcher.batch_save(li_u)

    pass




def main():

    create_1000_users_in_Parse()

    pass




if __name__ == '__main__':
    status = main()
    sys.exit(status)




































