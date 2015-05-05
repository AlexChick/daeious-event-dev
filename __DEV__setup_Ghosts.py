from __future__ import print_function
"""
"""

###############################################################################

# Import Python stuff
import itertools
import math
import os
import random
import sys
import time
from pprint import pprint

# Import Parse stuff
import httplib, json, urllib

# Import ParsePy stuff
from parse_rest.connection import ParseBatcher, register, SessionToken
from parse_rest.datatypes import ACL, Function, Object
from parse_rest.role import Role
from parse_rest.user import User

# Import my custom stuff
### (Nothing to see here yet!)

###############################################################################

def setup_ghosts(g):
    """
    Create 1 - 50 Ghost objects by "batch_save"-ing them to Parse using 
    ParsePy's ParseBatcher().

    """

    # Start a function timer.
    function_start_time = time.time()

    # We must subclass Object for the class names we want to use from Parse.
    class Ghost(Object):
        pass

    list_of_Ghost_objects_to_upload = []

    for ghost_number in range(1, g + 1, 1):
        new_Ghost_object = Ghost(
            username = "Ghost Partner",
            ghostNum = ghost_number,
            firstName = "Ghost",
            sex = "G",
            array_eventsRegistered = [1,2,3,4,5,6,7,8,9,10]
        )
        list_of_Ghost_objects_to_upload.append(new_Ghost_object)

    batcher = ParseBatcher()
    batcher.batch_save(list_of_Ghost_objects_to_upload)

    print ("\n{} Ghost objects uploaded to Parse in {} seconds.\n".format(g, time.time() - function_start_time))

###############################################################################

def main():
    setup_ghosts(37)
    return "setup_ghosts() has finished running."

###############################################################################

if __name__ == '__main__':
    status = main()
    sys.exit(status)

























