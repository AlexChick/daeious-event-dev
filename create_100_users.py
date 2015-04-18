"""
This program creates 100 test User objects by batch POSTing them to Parse.

"""

# import stuff
import math
import os
import random
import sqlite3
import time
import json, httplib
from pprint import pprint


# http://listofrandomnames.com/index.cfm?generated
fullNames_male = [
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
"Isidro Dublin"
]  

fullNames_female = [
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
"Olimpia Mcmeans"  
]






userCreator = open("100_users_v2.json", "w")

#userCreator.write("{ \"results\": [\n\n")

# Males

results_dict = { "results": [] }

for name in fullNames_male:
    object_dict = {
                      #"playerNum": playerCounter,
                      "username": name,
                      "bcryptPassword": "1234",
                      "array_eventsRegistered": [1,3,6],
                      "sex": 'M'
                    }
    results_dict['results'].append(object_dict)

for name in fullNames_female:
    object_dict = {
                      #"playerNum": playerCounter,
                      "username": name,
                      "bcryptPassword": "1234",
                      "array_eventsRegistered": [1],
                      "sex": 'F'
                    }

    results_dict['results'].append(object_dict)

results_dict_to_upload = json.dumps(results_dict)

userCreator.write(results_dict_to_upload)

userCreator.close()



""" This is copied from the Parse docs for batch object creation

import json, httplib
connection = httplib.HTTPSConnection('api.parse.com', 443)
connection.connect()
connection.request('POST', '/1/batch', json.dumps({
       "requests": [
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











