"""
"""

# Import Python stuff
from __future__ import print_function
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

def create_u_users(u, m = 50, f = 50):

    """
    """

    if m == f == 50:
        m = u/2
        f = u - u/2

    # Start a function timer.
    function_start_time = time.time()

    # Calling "register" allows parse_rest / ParsePy to work.
    # - register(APPLICATION_ID, REST_API_KEY, optional MASTER_KEY)
    register("AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS", master_key = "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv")

    m_names_dict = get_m_male_names_in_2_lists(m)
    f_names_dict = get_f_female_names_in_2_lists(f)
    full_names_dict = m_names_dict["m_full_names"] + f_names_dict["f_full_names"]
    first_names_dict = m_names_dict["m_first_names"] + f_names_dict["f_first_names"]

    user_upload_start_time = time.time()

    print ("\nSigning up {} users -- {} males and {} females.".format(u, m, f))

    for user_number in range(1, u + 1, 1):

        gender = "M" if (user_number <= m) else "F"

        array_events_registered = [1] if (user_number % 2 == 1) else [2]

        new_User_object = User.signup(
            full_names_dict[user_number - 1],
            "1234",
            userNum = user_number,
            firstName = first_names_dict[user_number - 1],
            sex = gender,
            array_eventsRegistered = array_events_registered
            )

        sys.stdout.write("\r{} of {} new users uploaded ({}{})".format(
            user_number, u, int(round((user_number*100.0)/u, 0)), "%"
            ))
        sys.stdout.flush()

    sys.stdout.write("\n") # move the cursor to the next line

    # Print results.
    function_total_time = round(time.time() - function_start_time, 3)

    print("\nFunction \"create_u_users({},{},{})\" ran in {} seconds."\
                .format(u, m, f, function_total_time))

    print ("\n\n{}\n{}\n{}\n{}\n{}\n{}\n\n".format(space_str, space_str, print_str, space_str, ast_str, und_str))

###############################################################################

def get_m_male_names_in_2_lists(m):

    """ 
    Return a dictionary of 2 lists of the first 'm' names from lists of
    randomly generated names. "m" is an int between 1 and 100 inclusive.
    """

    # 2 lists of 100 strings each: full and first names for males.
    # http://listofrandomnames.com/index.cfm?generated
    list_male_full_names = [
        "Hans Jacobsen","Nathanael Whitehorn","Everett Yarnall","Marcos Kennedy",
        "Ike Mees","Josiah Kucera","Cristopher Regalado","Ricky Minyard",
        "Lenard Breese","Erwin Cale","Dennis Litten","Ashley Mcgurk",
        "Bobbie Michaelson","Monty Levar","Cristobal Cangelosi","Jacinto Shotts",
        "Javier Duncan","Mohammad Crays","Leland Batista","Alexander Wilhelm",
        "Broderick Fields","Kennith Drees","Mitchel Oelke","Jeremy Bussard",
        "Casey Maynez","Karl Kirschbaum","Wilfredo Durkin","Warner Heatherly",
        "Enrique Ricken","Brian Wittig","Alexander Chau","Jamal Warden",
        "Jerome Copper","Rosendo Voegele","Hassan Tibbles","Earl Dorrance",
        "Teddy Organ","Dorian Barile","Devin Pendergraft","Freeman Coulston",
        "Booker Mcminn","Joan Brannen","Dallas Messmer","Miguel Bellefeuille",
        "Anthony Tillett","Donald Minier","Carson Lacour","Hubert Ellett", 
        "Rickey Lyon","Isidro Dublin","Enrique Chausse","Cristobal Vancamp",
        "Quintin Bramble","Edmundo Pooser","Landon Sells","Cary Allsup",
        "Timmy Fudge","Quentin Tay","Freddy Yant","Billie Lipp",
        "Shirley Paff","Monte Stetson","Samuel Perham","Kim Amo",
        "Jacob Yankey","Riley Lappin","Andy Houlihan","Arturo Remmers",
        "Millard Bachmann","Dylan Woodmansee","Neil Mccarter","Boyce Hurt",
        "Rickey Hebel","Dave Worthington","Weldon Nees","Jamaal Selman",
        "Austin Kuhlman","Val Neale","Titus Mickelson","Dorsey Northrup",
        "Roland Priddy","Antwan Conine","Wilburn Haner","Vern Reams",
        "Tanner Jacome","Milford Radebaugh","Vance Heap","Bert Carter",
        "Sang Brobst","Ellsworth Haws","Willard Cheers","Fredrick Luther",
        "Jeremiah Vicario","Bobbie Vanderhoff","Loren Soliday","John Stiverson",
        "Barney Hadley","David Wadleigh","Reuben Mccann","Darius Hunter"
    ]
    
    list_male_first_names = [
        "Hans","Nathanael","Everett","Marcos","Ike","Josiah","Cristopher","Ricky",
        "Lenard","Erwin","Dennis","Ashley","Bobbie","Monty","Cristobal","Jacinto",
        "Javier","Mohammad","Leland","Alexander","Broderick","Kennith","Mitchel","Jeremy",
        "Casey","Karl","Wilfredo","Warner","Enrique","Brian","Alexander","Jamal",
        "Jerome","Rosendo","Hassan","Earl","Teddy","Dorian","Devin","Freeman",
        "Booker","Joan","Dallas","Miguel","Anthony","Donald","Carson","Hubert",
        "Rickey","Isidro","Enrique","Cristobal","Quintin","Edmundo","Landon","Cary",
        "Timmy","Quentin","Freddy","Billie","Shirley","Monte","Samuel","Kim",
        "Jacob","Riley","Andy","Arturo","Millard","Dylan","Neil","Boyce",
        "Rickey","Dave","Weldon","Jamaal","Austin","Val","Titus","Dorsey",
        "Roland","Antwan","Wilburn","Vern","Tanner","Milford","Vance","Bert",
        "Sang","Ellsworth","Willard","Fredrick","Jeremiah","Bobbie","Loren","John",
        "Barney","David","Reuben","Darius"
    ]

    return {
                "m_full_names": list_male_full_names[:m], 
                "m_first_names": list_male_first_names[:m]
           }

###############################################################################

def get_f_female_names_in_2_lists(f):

    """ 
    Return a dictionary of 2 lists of the first 'f' names from lists of
    randomly generated names. "f" is an int between 1 and 100 inclusive.
    """

    # 2 lists of 100 strings each: full and first names for males.
    # http://listofrandomnames.com/index.cfm?generated
    list_female_full_names = [
        "Gillian Ayers","Celinda Mckillip","Tawana Lowe","Sixta Mccain",
        "Fabiola Goodman","Glendora Ganey","Kathaleen Furlong","Avis Mastin",
        "Ronna Sandifer","Temeka Northern","Malia Kovats","Rosie Kerfoot",
        "Alita Bublitz","Sherise Grosso","Aracely Harden","Tesha Strope",
        "Sharda Ricotta","Reda Frenette","Hilaria Thronson","Hannah Samuelson",
        "Nan Poythress","Andra Waddle","Jina Rausch","Elizabet Hennessy",
        "Lizzette Flippin","Peggy Mccollister","Lynnette Sund","Celesta Morning",
        "Shelly Haughey","Ching Mccarty","Yee Kelemen","Ilana Stromain",
        "Janel Demas","Tandy Hochman","Jonie Ceniceros","Summer Soles",
        "Kimberli Mannino","Stormy Simonton","Kirstie China","Mayme Labarre",
        "Mozelle Ranney","Mi Billingsley","Zofia Strauss","Kristian Kosinski",
        "Violet Robb","Darleen Feeney","Shavon Minogue","Tuyet Pridmore",
        "Rhea Bradish","Olimpia Mcmeans","Maren Ricciardi","Rosanna Legree",
        "Rebeca Farrier","Agripina Dillow","Adrien Lile","Ilda Burgoon",
        "Audrey Sobota","Deana Gallogly","Merry Condello","Alisa Carder",
        "Kimberely Greg","Carlotta Smalley","Toni Squier","Celeste Zane",
        "Collen Bart","Adrianne Bevins","Domitila Haworth","Kenia Wertman",
        "Daysi Banner","Delaine Chichester","Louise Strohmeyer","Burma Tuel",
        "Sadie Croxton","Mendy Dunham","Ginette Restrepo","Rana Gillard",
        "Slyvia Sommer","Lucretia Maggart","Raymonde Lazaro","Leone Leep",
        "Debora Londono","Malisa Tu","Carley Storie","Terrilyn Curci",
        "Layla Leandro","Floria Selvidge","Vannesa Phalen","Shawnta Osier",
        "Jin Aronowitz","Alia Gains","Carlota Godsey","Nakesha Coulter",
        "Galina Eanes","Cris Pontius","Staci Ocheltree","Elease Duenas",
        "Roberta Beshears","Dalila Eskew","Tia Dusenberry","Julia Ness"
    ]

    list_female_first_names = [
        "Gillian","Celinda","Tawana","Sixta","Fabiola","Glendora","Kathaleen","Avis",
        "Ronna","Temeka","Malia","Rosie","Alita","Sherise","Aracely","Tesha",
        "Sharda","Reda","Hilaria","Hannah","Nan","Andra","Jina","Elizabet",
        "Lizzette","Peggy","Lynnette","Celesta","Shelly","Ching","Yee","Ilana",
        "Janel","Tandy","Jonie","Summer","Kimberli","Stormy","Kirstie","Mayme",
        "Mozelle","Mi","Zofia","Kristian","Violet","Darleen","Shavon","Tuyet",
        "Rhea","Olimpia","Maren","Rosanna","Rebeca","Agripina","Adrien","Ilda",
        "Audrey","Deana","Merry","Alisa","Kimberely","Carlotta","Toni","Celeste",
        "Collen","Adrianne","Domitila","Kenia","Daysi","Delaine","Louise","Burma",
        "Sadie","Mendy","Ginette","Rana","Slyvia","Lucretia","Raymonde","Leone",
        "Debora","Malisa","Carley","Terrilyn","Layla","Floria","Vannesa","Shawnta",
        "Jin","Alia","Carlota","Nakesha","Galina","Cris","Staci","Elease",
        "Roberta","Dalila","Tia","Julia",
    ]

    return {
                "f_full_names": list_female_full_names[:f], 
                "f_first_names": list_female_first_names[:f]
           }

###############################################################################

def main():
    u = 37
    create_u_users(u)
    return "create_u_users({}) has finished running.".format(u)

###############################################################################

if __name__ == '__main__':
    status = main()
    sys.exit(status)









