"""
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

###############################################################################

def prepare_R1(m, f, mg, fg, ep, li_eu):
    """
    (males, females, male ghosts, female ghosts)

    Create Round-1 Interactions.

    For now, station Nums, iPad Nums, etc. start at 1, 2, 3, ...,
    but that will be changed so that the correct Nums are chosen 
    and put into lists.

    (It's tricky to do these random simulations because to make it realistic
        I'd have to pull only those objects with array_eventsRegistered 
        containing the eNum. To truly randomize things, I guess I could
        create an event with a random number of men and women every time...
        and while that seems like it's a lot more work, it also seems helpful
        in the long run -- testing will be easier, and the DEV program will
        be closer to the real thing. There's NO reason to rush into getting
        some kind of version of this completed...I've built a version before,
        so I already know I can do it. Now I just need to do it really well.
    """

    # Get the correct class names from the ep = Event Prefix (passed in).
    eventUser_ClassName = ep + "_User" # "zE####_User"
    eventUser_Class = Object.factory(eventUser_ClassName)

    eventIxnR1_ClassName = ep + "R1" # "zE####R1"
    eventIxnR1_Class = Object.factory(eventIxnR1_ClassName)

    ###
    ### Create all other vars and lists needed.
    ###

    # Calculate nums of stations, questions, and iPads from given parameters.
    s = m + mg
    i = s * 2
    q = s

    # Make lists of station nums and iPad nums, to be rotated between subrounds.
    li_staNums = list(x+1 for x in range(s))
    li_m_ipadNums = list(x+1 for x in range(0, s, 1))
    li_f_ipadNums = list(x+1 for x in range(s, 2*s, 1))
    li_qNums = list(x+1 for x in range(s))

    # Split the event user list into males and females; make enumeration useful
    # and list rotation between subrounds possible. Includes "ghosts."
    li_males = li_eu[:m+mg]
    li_females = li_eu[m+mg:]

    # Initiate interaction counter and list-to-upload.
    counter_ixn = 0
    li_R1_obj_to_upload = []

    # Iterate through the subrounds.
    for j in range(s): # s = stations, and also subrounds, as used here

        for k, eu_obj in enumerate(li_males):
            # enumerator goes through the male half (0-m)

            # increment the interaction counter
            counter_ixn += 1
        
            # create one interaction object
            new_ixn_object = eventIxnR1_Class(
                ixNum = counter_ixn,
                subNum = j + 1,
                staNum = li_staNums[k],
                m_userNum = li_males[k].event_userNum,
                f_userNum = li_females[k].event_userNum,
                m_user_objectId = li_males[k].user_objectId,
                f_user_objectId = li_females[k].user_objectId,
                m_thisEvent_objectId = li_males[k].objectId,
                f_thisEvent_objectId = li_females[k].objectId,
                m_ipadNum = li_m_ipadNums[k],
                f_ipadNum = li_f_ipadNums[k],
                qNum = li_qNums[k]
            )

            # add the object to a list to upload to Parse
            li_R1_obj_to_upload.append(new_ixn_object)

            # add the object to Firebase
            ### INSERT CODE HERE

        ###
        ### Rotate the lists between subrounds (in "for j in range(s)" loop).
        ###   (li_staNum will be iterated through correctly without alteration,
        ###   as will the lists of ipadNums.)
        ###

        # the m list will have its last item put in the front
        li_males = [li_males[-1]] + li_males[:-1]

        # the f list will have its first item put in the back
        li_females = li_females[1:] + [li_females[0]]

        # the qNums list happens to move the first two to the back
        li_qNums = li_qNums[2:] + li_qNums[:2]      

    ### END ITERATIONS ###

    # Save objects to Firebase, grouped by iPad.
    # Structure looks like:

    """

    "zE####R1_inx_obj_by_iPadNum": {

        "ipadNum_####": {

            "ixnNum_####": {

                "{}".format(li_R1_obj_to_upload.ixnNum): {

                    "subNum": li_R1_obj_to_upload.subNum,
                    "staNum": li_R1_obj_to_upload.staNum,
                    ...      

                }, 

                ...

            }, 

            ...
       
        }, 

        ...
    
    }

    """
    
    # Create references to Firebase.
    ref_root = Firebase('https://burning-fire-8681.firebaseio.com')
    ref_R1_ixn_objs_by_iPadNum = ref_root.child(
        '{}R1_inx_objs_by_iPadNum'.format(ep)
        )

    # Create references for all iPads, and put them in a dictionary
    dict_ref_ipadNum = {}
    for a in li_m_ipadNums + li_f_ipadNums:
        ref_ipadNum = ref_R1_ixn_objs_by_iPadNum.child('{}'.format(a))
        ref_ipadNum.patch(
            {
                "something": "goes here"
            })
        print ("iPad {} has been put into Firebase.".format(a))
        dict_ref_ipadNum["{}".format(ref_ipadNum)] = {}


    pprint(dict_ref_ipadNum)

    # Iterate through all objects, adding them to the right place in 
    # the dictionary, then upload the dictionary into Firebase
    for a in li_R1_obj_to_upload:
        correct_m_iPad = a.m_ipadNum
        correct_f_iPad = a.f_ipadNum
        #dict_ref_ipadNum[]




    # Save objects to Parse.
    # Call batcher.batch_save on slices of the list no larger than 50.
        # Parse will timeout if 1800 requests are made in 60 seconds,
        # hence the time.sleep(1.67) every 50 objects saved. I could probably
        # get away with sleeping less, but no reason to take chances.
    batcher = ParseBatcher()
    for b in range(counter_ixn/50 + 1):
        lo = 50*b
        hi = min(50 * (b+1), counter_ixn)
        batcher.batch_save(li_R1_obj_to_upload[lo:hi])

        sys.stdout.write("\r{} of {} new inx's uploaded ({}{})".format(
            50 + (50*b), 
            counter_ixn, 
            int(round((50*(b+1)*100.0)/counter_ixn, 0)), 
            "%"
            ))
        sys.stdout.flush() # must be done for it to work (why?)
        # time.sleep(1.67) # explained above

    sys.stdout.write("\n") # move the cursor to the next line after we're done



    # Create see-again-choice data-holding structure in Firebase.
    # Looks like:

    #     "see-again-choices-zE0001R1": {

            #     "event_users": {
                    
            #         "1": {
            #             "no": 12,
            #             "maybe-no": 1,
            #             "maybe-yes": 10,
            #             "yes": 4
            #         },

            #         "2": {
            #             "no": 2,
            #             "maybe-no": 5,
            #             "maybe-yes": 7,
            #             "yes": 13
            #         },    

            #         "3": { 
            #             "no": 8, 
            #             "maybe-no": 6,
            #             "maybe-yes": 3,
            #             "yes": 1
            #         },

            #         ...           
            #     }
            # }
























