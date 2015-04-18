"""
This program creates 200 _User and 50 Ghost objects
by "batch_save"-ing them to Parse using ParsePy's
ParseBatcher().

"""

# import stuff
import math
import os
import random
import sqlite3
import time
import json, httplib, urllib # parse stuff
from pprint import pprint # pretty printing
from parse_rest.connection import ParseBatcher, register, SessionToken
from parse_rest.datatypes import ACL, Function, Object
from parse_rest.role import Role
from parse_rest.user import User

program_start_time = time.time()

# Calling "register" allows parse_rest / ParsePy to work.
# - register(APPLICATION_ID, REST_API_KEY, optional MASTER_KEY)
register("AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS", master_key = "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv")

# We must subclass Object for the class names we want to use
class _User(Object):
    pass # don't need this (_User), as ParsePy has a special User.signup method
class Ghost(Object):
    pass


# http://listofrandomnames.com/index.cfm?generated
list_male_fullNames = [
"Hans Jacobsen",
"Nathanael Whitehorn",
"Everett Yarnall",
"Marcos Kennedy",
"Ike Mees",
"Josiah Kucera",
"Cristopher Regalado",
"Ricky Minyard",
"Lenard Breese",
"Erwin Cale",
"Dennis Litten",
"Ashley Mcgurk",
"Bobbie Michaelson",
"Monty Levar",
"Cristobal Cangelosi",
"Jacinto Shotts",
"Javier Duncan",
"Mohammad Crays",
"Leland Batista",
"Alexander Wilhelm",  
"Broderick Fields",  
"Kennith Drees",  
"Mitchel Oelke",  
"Jeremy Bussard",  
"Casey Maynez",
"Karl Kirschbaum",  
"Wilfredo Durkin",  
"Warner Heatherly",  
"Enrique Ricken",  
"Brian Wittig",  
"Alexander Chau",  
"Jamal Warden",  
"Jerome Copper",  
"Rosendo Voegele",  
"Hassan Tibbles",  
"Earl Dorrance",  
"Teddy Organ",  
"Dorian Barile",  
"Devin Pendergraft",  
"Freeman Coulston",  
"Booker Mcminn",  
"Joan Brannen",  
"Dallas Messmer",  
"Miguel Bellefeuille",  
"Anthony Tillett",  
"Donald Minier",  
"Carson Lacour",  
"Hubert Ellett", 
"Rickey Lyon",  
"Isidro Dublin",
"Enrique Chausse",
"Cristobal Vancamp",
"Quintin Bramble",
"Edmundo Pooser",
"Landon Sells",
"Cary Allsup",
"Timmy Fudge",
"Quentin Tay",
"Freddy Yant",
"Billie Lipp",
"Shirley Paff",
"Monte Stetson",
"Samuel Perham",
"Kim Amo",
"Jacob Yankey",
"Riley Lappin",
"Andy Houlihan",
"Arturo Remmers",
"Millard Bachmann",
"Dylan Woodmansee",
"Neil Mccarter",
"Boyce Hurt",
"Rickey Hebel",
"Dave Worthington",
"Weldon Nees",
"Jamaal Selman",
"Austin Kuhlman",
"Val Neale",
"Titus Mickelson",
"Dorsey Northrup",
"Roland Priddy",
"Antwan Conine",
"Wilburn Haner",
"Vern Reams",
"Tanner Jacome",
"Milford Radebaugh",
"Vance Heap",
"Bert Carter",
"Sang Brobst",
"Ellsworth Haws",
"Willard Cheers",
"Fredrick Luther",
"Jeremiah Vicario",
"Bobbie Vanderhoff",
"Loren Soliday",
"John Stiverson",
"Barney Hadley",
"David Wadleigh",
"Reuben Mccann",
"Darius Hunter"
]

list_male_firstNames = [
"Hans",
"Nathanael",
"Everett",
"Marcos",
"Ike",
"Josiah",
"Cristopher",
"Ricky",
"Lenard",
"Erwin",
"Dennis",
"Ashley",
"Bobbie",
"Monty",
"Cristobal",
"Jacinto",
"Javier",
"Mohammad",
"Leland",
"Alexander",
"Broderick",
"Kennith",
"Mitchel",
"Jeremy",
"Casey",
"Karl",
"Wilfredo",
"Warner",
"Enrique",
"Brian",
"Alexander",
"Jamal",
"Jerome",
"Rosendo",
"Hassan",
"Earl",
"Teddy",
"Dorian",
"Devin",
"Freeman",
"Booker",
"Joan",
"Dallas",
"Miguel",
"Anthony",
"Donald",
"Carson",
"Hubert",
"Rickey",
"Isidro",
"Enrique",
"Cristobal",
"Quintin",
"Edmundo",
"Landon",
"Cary",
"Timmy",
"Quentin",
"Freddy",
"Billie",
"Shirley",
"Monte",
"Samuel",
"Kim",
"Jacob",
"Riley",
"Andy",
"Arturo",
"Millard",
"Dylan",
"Neil",
"Boyce",
"Rickey",
"Dave",
"Weldon",
"Jamaal",
"Austin",
"Val",
"Titus",
"Dorsey",
"Roland",
"Antwan",
"Wilburn",
"Vern",
"Tanner",
"Milford",
"Vance",
"Bert",
"Sang",
"Ellsworth",
"Willard",
"Fredrick",
"Jeremiah",
"Bobbie",
"Loren",
"John",
"Barney",
"David",
"Reuben",
"Darius"
]

list_female_fullNames = [
"Gillian Ayers",  
"Celinda Mckillip",  
"Tawana Lowe",  
"Sixta Mccain",  
"Fabiola Goodman",  
"Glendora Ganey",  
"Kathaleen Furlong",  
"Avis Mastin",  
"Ronna Sandifer",  
"Temeka Northern",  
"Malia Kovats",  
"Rosie Kerfoot",  
"Alita Bublitz",  
"Sherise Grosso",  
"Aracely Harden",  
"Tesha Strope",  
"Sharda Ricotta",  
"Reda Frenette",  
"Hilaria Thronson",  
"Hannah Samuelson",  
"Nan Poythress",  
"Andra Waddle",  
"Jina Rausch",  
"Elizabet Hennessy",  
"Lizzette Flippin",  
"Peggy Mccollister",  
"Lynnette Sund",  
"Celesta Morning",  
"Shelly Haughey",  
"Ching Mccarty",  
"Yee Kelemen",  
"Ilana Stromain",  
"Janel Demas",  
"Tandy Hochman",  
"Jonie Ceniceros",  
"Summer Soles",  
"Kimberli Mannino",  
"Stormy Simonton",  
"Kirstie China",  
"Mayme Labarre",  
"Mozelle Ranney",  
"Mi Billingsley",  
"Zofia Strauss",  
"Kristian Kosinski",  
"Violet Robb",  
"Darleen Feeney",  
"Shavon Minogue",  
"Tuyet Pridmore",  
"Rhea Bradish",  
"Olimpia Mcmeans",
"Maren Ricciardi",
"Rosanna Legree",
"Rebeca Farrier",
"Agripina Dillow",
"Adrien Lile",
"Ilda Burgoon",
"Audrey Sobota",
"Deana Gallogly",
"Merry Condello",
"Alisa Carder",
"Kimberely Greg",
"Carlotta Smalley",
"Toni Squier",
"Celeste Zane",
"Collen Bart",
"Adrianne Bevins",
"Domitila Haworth",
"Kenia Wertman",
"Daysi Banner",
"Delaine Chichester",
"Louise Strohmeyer",
"Burma Tuel",
"Sadie Croxton",
"Mendy Dunham",
"Ginette Restrepo",
"Rana Gillard",
"Slyvia Sommer",
"Lucretia Maggart",
"Raymonde Lazaro",
"Leone Leep",
"Debora Londono",
"Malisa Tu",
"Carley Storie",
"Terrilyn Curci",
"Layla Leandro",
"Floria Selvidge",
"Vannesa Phalen",
"Shawnta Osier",
"Jin Aronowitz",
"Alia Gains",
"Carlota Godsey",
"Nakesha Coulter",
"Galina Eanes",
"Cris Pontius",
"Staci Ocheltree",
"Elease Duenas",
"Roberta Beshears",
"Dalila Eskew",
"Tia Dusenberry",
"Julia Ness"
]

list_female_firstNames = [
"Gillian",
"Celinda",
"Tawana",
"Sixta",
"Fabiola",
"Glendora",
"Kathaleen",
"Avis",
"Ronna",
"Temeka",
"Malia",
"Rosie",
"Alita",
"Sherise",
"Aracely",
"Tesha",
"Sharda",
"Reda",
"Hilaria",
"Hannah",
"Nan",
"Andra",
"Jina",
"Elizabet",
"Lizzette",
"Peggy",
"Lynnette",
"Celesta",
"Shelly",
"Ching",
"Yee",
"Ilana",
"Janel",
"Tandy",
"Jonie",
"Summer",
"Kimberli",
"Stormy",
"Kirstie",
"Mayme",
"Mozelle",
"Mi",
"Zofia",
"Kristian",
"Violet",
"Darleen",
"Shavon",
"Tuyet",
"Rhea",
"Olimpia",
"Maren",
"Rosanna",
"Rebeca",
"Agripina",
"Adrien",
"Ilda",
"Audrey",
"Deana",
"Merry",
"Alisa",
"Kimberely",
"Carlotta",
"Toni",
"Celeste",
"Collen",
"Adrianne",
"Domitila",
"Kenia",
"Daysi",
"Delaine",
"Louise",
"Burma",
"Sadie",
"Mendy",
"Ginette",
"Rana",
"Slyvia",
"Lucretia",
"Raymonde",
"Leone",
"Debora",
"Malisa",
"Carley",
"Terrilyn",
"Layla",
"Floria",
"Vannesa",
"Shawnta",
"Jin",
"Alia",
"Carlota",
"Nakesha",
"Galina",
"Cris",
"Staci",
"Elease",
"Roberta",
"Dalila",
"Tia",
"Julia",
]

list_ghost_fullNames = ["Ghost Partner"] * 50
list_ghost_firstNames = ["Ghost"] * 50

# # Parse batch limit is 50, so we have to split up the larger lists

# # males
# list_male_fullNames_1 = list_male_fullNames[:50] # takes indices 0-49
# list_male_fullNames_2 = list_male_fullNames[50:] # takes indices 50-99
# list_male_firstNames_1 = list_male_firstNames[:50]
# list_male_firstNames_2 = list_male_firstNames[50:]

# # females
# list_female_fullNames_1 = list_female_fullNames[:50] # takes indices 0-49
# list_female_fullNames_2 = list_female_fullNames[50:] # takes indices 50-99
# list_female_firstNames_1 = list_female_firstNames[:50]
# list_female_firstNames_2 = list_female_firstNames[50:]

# print len(list_male_fullNames_1)
# print len(list_male_fullNames_2)
# print len(list_male_firstNames_1)
# print len(list_male_firstNames_2)

userCounter = 0
ghostCounter = 0

list_iterator = 0

#list_of_users_to_upload = []
list_of_ghosts_to_upload = []

tuple_of_lists = (list_male_fullNames, list_female_fullNames, list_ghost_fullNames)


for name_list in tuple_of_lists:

    if list_iterator == 0:
        sex = 'M'
        firstName_list = list_male_firstNames

    elif list_iterator == 1:
        sex = 'F'
        firstName_list = list_female_firstNames

    else:
        sex = 'G'
        firstName_list = list_ghost_firstNames


    for name in name_list:

        if list_iterator != 2:

            userCounter += 1

            eventsRegistered_list = [1,8,12,23] if name_list.index(name) < 50 else [2,7,15,24]

            # new_user_object_dict = {
            #                 "method": "POST",
            #                 "path": "/1/users",
            #                 "body": 
            #                 {
            #                   "username": name,
            #                   "bcryptPassword": "1234",
            #                   "userNum": userCounter,
            #                   "sex": sex,
            #                   "array_eventsRegistered": eventsRegistered_list
            #                 }
            # }

            # list_of_users_to_upload.append(new_user_object_dict)

            # The User.signup function is really slow.
            # It might be better to use a direct batch without ParsePy.
            # (Tried that...couldn't get it to work. At least this works.)
            user_upload_start_time = time.time()

            new_User = User.signup(name, "1234",
                userNum = userCounter,
                firstName = firstName_list[name_list.index(name)],
                sex = sex,
                array_eventsRegistered = eventsRegistered_list
            )
                
            print "User with userNum {} created and uploaded to _User in Parse in {} seconds.".format(userCounter, time.time() - user_upload_start_time)

        else:

            ghostCounter += 1

            new_Ghost = Ghost(
                username = "Ghost Partner",
                ghostNum = ghostCounter,
                firstName = "Ghost",
                sex = sex,
                array_eventsRegistered = []
            )

            list_of_ghosts_to_upload.append(new_Ghost)

    list_iterator += 1


# # upload _User objects

# requests_list_to_upload_1 = list_of_users_to_upload[0:50]
# requests_list_to_upload_2 = list_of_users_to_upload[50:100]
# requests_list_to_upload_3 = list_of_users_to_upload[100:150]
# requests_list_to_upload_4 = list_of_users_to_upload[150:200]

# tuple_requests_lists = (requests_list_to_upload_1, 
#                         requests_list_to_upload_2,
#                         requests_list_to_upload_3,
#                         requests_list_to_upload_4)

# batch_upload_counter = 0

# for requests_list in tuple_requests_lists:
#     connection = httplib.HTTPSConnection('api.parse.com', 443)
#     connection.connect()
#     connection.request('POST', '/1/batch', json.dumps({
#         "requests": requests_list
#         }), {
#            "X-Parse-Application-Id": "AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ",
#            "X-Parse-Master-Key": "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv",
#            "Content-Type": "application/json"
#          })
#     creation_result = json.loads(connection.getresponse().read())
#     batch_upload_counter += 1
#     print "Batch {} of 4 containing {} _User objects uploaded to Parse.\n".format(
#         batch_upload_counter, len(creation_result))



# upload Ghost objects
batcher = ParseBatcher()
batcher.batch_save(list_of_ghosts_to_upload)
print "\nBatch 1 of 1 containing 50 Ghost objects uploaded to Parse.\n"

print "Program complete.\n"

print "Program time: {} seconds.\n".format(time.time() - program_start_time)

"""
TIME TEST results

Program time: 67.3509368896 seconds.


"""







# userCreator = open("100_users_v2.json", "w")

# #userCreator.write("{ \"results\": [\n\n")

# # Males

# results_dict = { "results": [] }

# for name in fullNames_male:
#     object_dict = {
#                       #"playerNum": playerCounter,
#                       "username": name,
#                       "bcryptPassword": "1234",
#                       "array_eventsRegistered": [1,3,6],
#                       "sex": 'M'
#                     }
#     results_dict['results'].append(object_dict)

# for name in fullNames_female:
#     object_dict = {
#                       #"playerNum": playerCounter,
#                       "username": name,
#                       "bcryptPassword": "1234",
#                       "array_eventsRegistered": [1],
#                       "sex": 'F'
#                     }

#     results_dict['results'].append(object_dict)

# results_dict_to_upload = json.dumps(results_dict)

# userCreator.write(results_dict_to_upload)

# userCreator.close()



""" This is copied from the Parse docs for batch object creation

import json, httplib
connection = httplib.HTTPSConnection('api.parse.com', 443)
connection.connect()
connection.request('POST', '/1/batch', json.dumps({
       "results": [
         {
           "method": "POST",
           "path": "/1/classes/_User",
           "body": 
           {
             "username"  : "alexchick",
             "password"  : "1234",
             "firstName" : "Alex",
             "lastName"  : "Chick", 
           }
         },
         {
           "method": "POST",
           "path": "/1/classes/Event",
           "body": {
             "eventNumber" : 0002,
             "location"	   : "San Francisco",
             "start"	   : ["2016.10.24","20:00"]
           }
         }
       ]
     }), {
       "X-Parse-Application-Id": "AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ",
       "X-Parse-REST-API-Key": "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS",
       "Content-Type": "application/json"
     })
result = json.loads(connection.getresponse().read())
print result

"""











