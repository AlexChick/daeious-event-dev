from __future__ import print_function
"""
This program creates 100 test Question objects (with a 4-answer array)
and uploads them to Parse.
"""

###############################################################################
"""                                 IMPORTS                                 """
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
###

###############################################################################
"""                                FUNCTIONS                                """
###############################################################################

def setup_questions(q):

    """
    """

    # Start a function timer.
    function_start_time = time.time()

    # We must subclass Object for the class names we want to use.
    class Question(Object):
        pass

    # Print the "function is starting" message.
    # (Later, I'd like to make a decorator that does this.)
    print("\nFunction \"setup_questions({})\" is now running.".format(q))
    
    # Instantiate the list to upload.
    list_Question_objects_to_upload = []

    # Get a list of "q" questions and a list of "q" 4-answer lists.
    list_q_question_strings = get_q_question_strings(q)
    list_q_answer_lists = get_q_answer_lists(q)

    # # Initialize the question counter.
    # question_counter = 0

    # Create new Question objects and put them into a big ol' list.
    for index, question_str in enumerate(list_q_question_strings):

        new_Question_object = Question(
            questionNum = index + 1,
            questionText = question_str,
            answersArray = list_q_answer_lists[index]
            )

        list_Question_objects_to_upload.append(new_Question_object)

    # Upload the list of new iPad objects to Parse.
    # The Parse batch request limit is 50, 
    #     and the Parse request limit is 30/sec = 1800/min.
    # Other functions are being run surrounding this, so to avoid going over
    #     the 1800/min limit, call time.sleep(q/30 - time_spent_uploading). 

    
    # Create a ParseBatcher object.
    batcher = ParseBatcher()

    print("\n{} Question objects are being uploaded...".format(q))

    # Start an "uploading" timer.
    uploading_start_time = time.time()

    # Call batcher.batch_save on slices of the list no larger than 50.
    for k in range(q/50 + 1):
        ### lower = 50*k
        ### upper = 
        try:
            batcher.batch_save(list_Question_objects_to_upload[
                50*k : 50*(k + 1)
                ])
        except:
            batcher.batch_save(list_Question_objects_to_upload[
                50*k : q
                ])

    # Calculate time spent uploading and how long to sleep for.
    time_spent_uploading = time.time() - uploading_start_time
    how_long_to_sleep_for = (q/30.0) - time_spent_uploading
    how_long_to_sleep_for_rounded = round(how_long_to_sleep_for, 3)
    print ("\nUploading took {} seconds.".format(round(time_spent_uploading, 3)))

    # Sleep.
    for k in range(1, 101, 1):
        sys.stdout.write("\r{}{} of {}s sleep complete.".format(k, "%", 
            how_long_to_sleep_for_rounded)
            ) # \r puts cursor back to start of line i/o onto the next line
        sys.stdout.flush() # this must be called to refresh the line
        time.sleep(how_long_to_sleep_for / 100.0)
    sys.stdout.write("\n") # move the cursor to the next line

    # Print results.
    function_total_time = round(time.time() - function_start_time, 3)

    print ("\n\
            \n***********************************************************************\
            \n*****                                                             *****\
            \n*****   Function \"setup_questions({})\" ran in {} seconds.   *****\
            \n*****                                                             *****\
            \n***********************************************************************\
            \n_______________________________________________________________________\
            \n=======================================================================\
            \n\n\
            ".format(q, function_total_time))

###############################################################################

def get_q_question_strings(q):

    """ 
    Return a list of the first 'q' question strings 
    from a large list of randomly generated questions.
    
    --- 's' is an int between 1 and 100 inclusive.

    """

    # 100 randomly generated questions from 
    # http://www.cfcl.com/vlb/Memes/Questionaires/random_1.html
    list_100_questions = [
    "Grab the book nearest to you, turn to page 18, and find line 4. \
        What does it say?",
    "Stretch your left arm out as far as you can, What can you touch?",
    "Before you started this survey, what were you doing?",
    "What is the last thing you watched on TV?",
    "Without looking, guess what time it is.",
    "Now look at the clock. What is the actual time?",
    "With the exception of the computer, what can you hear?",
    "When did you last step outside? What were you doing?",
    "Did you dream last night?",
    "Do you remember your dreams?",
    "When did you last laugh?",
    "Do you remember your childhood?",
    "What is on the walls of the room you are in?",
    "Seen anything weird lately?",
    "What do you think of this quiz?",
    "What is the last film you saw?",
    "If you could live anywhere in the world, where would you live?",
    "If you became a multi-millionaire overnight, what would you buy?",
    "Tell me something about you that most people don't know.",
    "If you could change one thing about the world, what would you do?",
    "Do you like to dance?",
    "Would you ever consider living abroad?",
    "Does your name make any interesting anagrams?",
    "Who made the last incoming call on your phone?",
    "What is the last thing you downloaded onto your computer?",
    "Last time you swam in a pool?",
    "Type of music you like most?",
    "Type of music you dislike most?",
    "Are you listening to music right now?",
    "What color is your bedroom carpet?",
    "If you could change something about your home, \
        without worry about expense or mess, what would you do?",
    "What was the last thing you bought?",
    "Have you ever ridden on a motorbike?",
    "Would you go bungee jumping or sky diving?",
    "Do you have a garden?",
    "Do you really know all the words to your national anthem?",
    "What is the first thing you think of when you wake up in the morning?",
    "If you could eat lunch with one famous person, who would it be?",
    "Who sent the last text message you received?",
    "Which store would you choose to max out your credit card?",
    "What time is bed time?",
    "Have you ever been in a beauty pageant?",
    "How many tattoos do you have?",
    "If you don't have any, have you ever thought of getting one?",
    "What did you do for your last birthday?",
    "Do you carry a donor card?",
    "Who was the last person you ate dinner with?",
    "Is the glass half empty or half full?",
    "What's the farthest-away place you've been?",
    "When's the last time you ate a homegrown tomato?",
    "Have you ever won a trophy?",
    "Are you a good cook?",
    "Do you know how to pump your own gas?",
    "If you could meet any one person (from history or currently alive), \
        who would it be?",
    "Have you ever had to wear a uniform to school?",
    "Do you touch-type?",
    "What's under your bed?",
    "Do you believe in love at first sight?",
    "Think fast, what do you like right now?",
    "Where were you on Valentine's day?",
    "What time do you get up?",
    "What was the name of your first pet?",
    "Who is the second to last person to call you?",
    "Is there anything going on this weekend?",
    "How are you feeling right now?",
    "What do you think about the most?",
    "What time do you get up in the morning?",
    "If you had A Big Win in the Lottery, how long would you wait \
        to tell people?",
    "Who would you tell first?",
    "What is the last movie that you saw at the cinema?",
    "Do you sing in the shower?",
    "Which store would you choose to max out your credit card?",
    "What do you do most when you are bored?",
    "What do you do for a living?",
    "Do you love your job?",
    "What did you want to be when you grew up?",
    "If you could have any job, what would you want to do/be?",
    "Which came first the chicken or the egg?",
    "How many keys on your key ring?",
    "Where would you retire to?",
    "What kind of car do you drive?",
    "What are your best physical features?",
    "What are your best characteristics?",
    "If you could go anywhere in the world on vacation where would you go?",
    "What kind of books do you like to read?",
    "Where would you want to retire to?",
    "What is your favorite time of the day?",
    "Where did you grow up?",
    "How far away from your birthplace do you live now?",
    "What are you reading now?",
    "Are you a morning person or a night owl?",
    "Can you touch your nose with your tongue?",
    "Can you close your eyes and raise your eyebrows?",
    "Do you have pets?",
    "How many rings before you answer the phone?",
    "What is your best childhood memory?",
    "What are some of the different jobs that you have had in your life?",
    "Any new and exciting things that you would like to share?",
    "What is most important in life?",
    "What Inspires You?"
    ]

    return list_100_questions[:q]

###############################################################################

def get_q_answer_lists(a):

    """ 
    Return a list of the first 'a' lists of 4 answers 
    from a large list of lists of randomly generated words.
            
    --- 's' is an int between 1 and 100 inclusive.

    """

    # a 100-item list of 4-item lists.
    # https://www.randomlists.com/random-words
    list_100_lists_of_4_answers = [
    ["force","own","waggish","romantic"],
    ["sleep","tangy","deliver","sneeze"],
    ["goofy","death","abhorrent","unwieldy"],
    ["report","wary","frame","sad"],
    ["surprise","wistful","thumb","chase"],
    ["stereotyped","fine","first","robust"],
    ["fog","disastrous","attack","glove"],
    ["slimy","remember","fabulous","square"],
    ["correct","gray","real","transport"],
    ["eggs","stove","liquid","tumble"],
    ["lock","tacit","monkey","religion"],
    ["bubble","high","juice","escape"],
    ["soothe","dirty","simple","guess"],
    ["wall","deer","paddle","stupid"],
    ["learn","poison","preserve","squeamish"],
    ["language","separate","wild","class"],
    ["adjustment","snails","abrupt","loud"],
    ["knowing","tick","field","subsequent"],
    ["towering","forgetful","important","announce"],
    ["impartial","cracker","meat","wish"],
    ["clumsy","dull","birthday","value"],
    ["rock","true","awful","fly"],
    ["accept","sponge","invent","wretched"],
    ["sneeze","scrub","waste","thinkable"],
    ["control","itch","puny","fold"],
    ["crabby","punch","dam","adhesive"],
    ["floating","can","transport","stream"],
    ["surprise","reflect","idea","straw"],
    ["prevent","feeling","tap","poor"],
    ["melodic","space","silky","fish"],
    ["longing","nippy","crime","label"],
    ["puffy","neat","standing","abnormal"],
    ["pinch","sail","abortive","curious"],
    ["tasteless","certain","encourage","vast"],
    ["impulse","subtract","taste","thoughtful"],
    ["songs","wing","ultra","mere"],
    ["shake","yielding","skate","learned"],
    ["classy","profit","fixed","guttural"],
    ["save","merciful","blush","gusty"],
    ["wrathful","alive","matter","unwritten"],
    ["soap","purring","rambunctious","female"],
    ["nosy","carpenter","spiteful","bag"],
    ["lewd","sail","deeply","cow"],
    ["bat","filthy","anger","cause"],
    ["greedy","pastoral","cycle","vase"],
    ["adamant","dogs","youthful","throat"],
    ["woman","blot","lunch","creature"],
    ["chess","camp","time","oven"],
    ["thaw","offbeat","voice","pan"],
    ["unbiased","quaint","powder","fact"],
    ["girl","acoustics","uncle","rifle"],
    ["shivering","synonymous","week","hungry"],
    ["damp","lumber","auspicious","umbrella"],
    ["limping","quiet","painful","complicated"],
    ["smart","proud","obsequious","cake"],
    ["hunt","assorted","seemly","shade"],
    ["oval","ritzy","stick","foot"],
    ["ruddy","boorish","wax","crib"],
    ["way","girls","nutty","bump"],
    ["grandfather","vacuous","degree","gruesome"],
    ["jittery","unkempt","supreme","moan"],
    ["stomach","comfortable","poke","note"],
    ["superb","snow","produce","heavy"],
    ["mind","well-groomed","dinner","sky"],
    ["grass","silent","puncture","quilt"],
    ["name","shy","overconfident","offer"],
    ["mouth","toothbrush","juvenile","feeble"],
    ["typical","dance","quizzical","friends"],
    ["regret","name","oil","rabid"],
    ["frogs","quirky","natural","tough"],
    ["abusive","maid","flower","meek"],
    ["frantic","writer","coach","grab"],
    ["lyrical","wide-eyed","burn","end"],
    ["lean","flowery","bead","tug"],
    ["wren","exciting","earthy","delirious"],
    ["debt","sordid","whirl","town"],
    ["locket","ten","rescue","muscle"],
    ["volatile","cub","quick","equable"],
    ["frightened","cup","trail","pack"],
    ["desire","effect","disagree","pretend"],
    ["squeak","guide","unadvised","ocean"],
    ["retire","telling","babies","arrange"],
    ["frame","grade","dramatic","humdrum"],
    ["men","nebulous","violent","muddle"],
    ["scientific","gainful","remind","internal"],
    ["fear","kaput","battle","pig"],
    ["settle","ruthless","position","changeable"],
    ["spot","fluffy","argument","addition"],
    ["substance","paltry","safe","energetic"],
    ["bottle","fast","bird","obese"],
    ["famous","unequaled","even","vivacious"],
    ["unite","scare","silver","loaf"],
    ["jealous","number","examine","graceful"],
    ["premium","various","insect","torpid"],
    ["brawny","scrape","cheat","tree"],
    ["sleepy","beds","sincere","abashed"],
    ["knit","hammer","whistle","fireman"],
    ["trip","disturbed","birth","meeting"],
    ["slave","boy","sturdy","form"],
    ["anxious","jam","whip","cynical"]
    ]

    return list_100_lists_of_4_answers[:a]

###############################################################################

def main():

    setup_ipads(200)
    #pprint(get_s_ipad_serial_numbers(s))

###############################################################################

if __name__ == '__main__':
    main()























