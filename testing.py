# Import Python stuff.
from __future__ import print_function # apparently, has to be on first line
from datetime import datetime
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
import daeious
from helpers import batch_delete_from_Parse_all_objects_of_class
from helpers import batch_query
from helpers import batch_upload_to_Parse
from helpers import create_QA_database_in_Firebase
from helpers import create_SAC_database_in_Firebase
from helpers import filter_by_value
from helpers import mk_serial
from helpers import register_with_Parse





register_with_Parse()



# Logging

# # define a Handler which writes ERROR messages or higher to the sys.stderr
# console = logging.StreamHandler()
# # set up logging to file - see previous section for more details
# logging.basicConfig(level=logging.ERROR,
#                     #format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#                     datefmt='%m-%d %H:%M',
#                     filename='',
#                     filemode='w')
# # set a format which is simpler for console use
# formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# # tell the handler to use this format
# console.setFormatter(formatter)
# # add the handler to the root logger
# #logging.getLogger('').addHandler(console)
logging.getLogger('').addHandler(logging.StreamHandler())

#logging.error("\n\n\n\n\n      (Oops! Too many requests to Parse again!)\n\n\n\n\n")

################################################################################
################################################################################
################################################################################

# li_times = []

# for i in range(2):
#   li_times.append(daeious.main())
#   # if i == 0:
#   #   time.sleep(10)

# print (li_times)
# pprint(li_times)
# print ("\nAverage time: {}\n".format(sum(li_times)/len(li_times)))

e0 = daeious._Event(EVENT_NUMBER = 0,
           START_AT_ROUND = 0,
           MEN = 20,
           WOMEN = 20,
           SEC_PER_R1_IX = 20,
           SEC_PER_R2_IX = 40,
           SEC_PER_R3_IX = 60)

e1 = daeious._Event(EVENT_NUMBER = 1,
           START_AT_ROUND = 0,
           MEN = 20,
           WOMEN = 20,
           SEC_PER_R1_IX = 20,
           SEC_PER_R2_IX = 40,
           SEC_PER_R3_IX = 60)

e2 = daeious._Event(EVENT_NUMBER = 2,
           START_AT_ROUND = 0,
           MEN = 20,
           WOMEN = 20,
           SEC_PER_R1_IX = 20,
           SEC_PER_R2_IX = 40,
           SEC_PER_R3_IX = 60)



print ("e0 MEN:", e0.num_m_eu_p)
assert e0.num_m_eu_p == 20

e0.num_m_eu_p += 1

print ("e0 MEN:", e0.num_m_eu_p)
assert e0.num_m_eu_p == 21

li = [e0, e1, e2]
li[0].num_m_eu_p = 24
for index, e in enumerate(li):
    print (e.event_number)
    assert e.event_number == index

for index, e in enumerate(li):
    print (e.num_m_eu_p, 100)
    #assert e.num_m_eu_p == index

for e in filter_by_value(li, 1):
    pass

li_evNum = list(filter_by_value(li, 1))

for event in li_evNum:
    print(event.event_number, 200)

class Interaction(object):
    
    COUNTER = 0

    def __init__(self):
        Interaction.COUNTER += 1
        self.ix_num = Interaction.COUNTER
        pass

    def simulate(self):
        #self.m_see_f = random.choice(["no", "maybe-no", "maybe-yes", "yes"])
        #self.f_see_m = random.choice(["no", "maybe-no", "maybe-yes", "yes"])
        self.m_see_f = random.randint(1, 4)
        self.f_see_m = random.randint(1, 4)
        #self.same = (self.m_see_f == self.f_see_m)
        self.agree = 1 if self.m_see_f == self.f_see_m else 0
        pass

    def __iter__(self):
        # first start by grabbing the Class items
        iters = dict((x,y) for x,y in Interaction.__dict__.items() 
            if x[:2] != '__' 
            and x != "simulate"
            and x != "COUNTER"
            )
        # then update the class items with the instance items
        iters.update(self.__dict__)
        # now 'yield' through the items
        for x,y in iters.items():
            yield x,y

    # def __repr__(self):
    #     pass

    pass

li_ix_obj = []

for n in range(2601):
    ix = Interaction()
    ix.simulate()
    li_ix_obj.append(ix)

li_ix_with_even_ix_num = list(filter_by_value(li_ix_obj, 2))
evens = len(li_ix_with_even_ix_num)
print (evens, 300)
assert evens == 1300

for ix in li_ix_obj:
    print (dict(ix))

#print (["\n{}\n".format(dict(ix)) for ix in li_ix_obj])

for ix in li_ix_obj:
    if ix.ix_num % 2 == 1:
        ix.ix_num = 0
    #print (dict(ix))

li_ix_with_even_ix_num = list(filter_by_value(li_ix_obj, 2))
evens = len(li_ix_with_even_ix_num)
print (evens, 400)
assert evens == 2601

count = 0
for ix in li_ix_obj:
    if ix.agree == 1:
        count += 1

print("{}/2601 = {}%".format(count, round(100*count/2601.0, 3)))





style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
    num_format_str='#,##0.00')
style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

wb = xlwt.Workbook()
ws = wb.add_sheet('A Test Sheet')

ws.write(0, 0, 1234.56, style0)
ws.write(1, 0, datetime.now(), style1)
ws.write(2, 0, 1)
ws.write(2, 1, 1)
ws.write(2, 2, xlwt.Formula("A3+B3"))

wb.save('example.xls')

print (dict(li_ix_obj[0]).keys())

for c, label in enumerate(dict(li_ix_obj[0]).keys()):
    ws.write(5, c, label)

wb.save('example.xls')

for c, label in enumerate(dict(li_ix_obj[0]).keys()):
    for r, ix in enumerate(li_ix_obj):
        ws.write(r+6, c, getattr(ix, label))

wb.save('example.xls')









































