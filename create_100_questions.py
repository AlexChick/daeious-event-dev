"""
This program creates 100 test Question objects (with a 4-answer array)
and uploads them to Parse.

"""

# import stuff
import math
import os
import random
import sqlite3
import time
import json, httplib
from pprint import pprint

# http://www.cfcl.com/vlb/Memes/Questionaires/random_1.html
questions_list = [
"Grab the book nearest to you, turn to page 18, and find line 4. What does it say?",
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
"If you could change one thing about the world, regardless of guilt or politics, what would you do?",
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
"If you could change something about your home, without worry about expense or mess, what would you do?",
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
"If you could meet any one person (from history or currently alive), who would it be?",
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
"If you had A Big Win in the Lottery, how long would you wait to tell people?",
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

# a 100-item list of 4-item lists.
# https://www.randomlists.com/random-words
answers_list_of_lists = [
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


chunk_q1 = questions_list[:50]
chunk_q2 = questions_list[50:]
chunk_a1 = answers_list_of_lists[:50]
chunk_a2 = answers_list_of_lists[50:]

questions_chunk = [chunk_q1, chunk_q2]

question_counter = 1


for chunk in questions_chunk:

    requests_array = []

    for question_string in chunk: 

        new_question_object_dict = {
                        "method": "POST",
                        "path": "/1/classes/Question",
                        "body": 
                        {
                          "questionText": question_string,
                          "answersArray": answers_list_of_lists[0],
                          "questionNum": question_counter
                        }
        }

        requests_array.append(new_question_object_dict)

        answers_list_of_lists.pop(0)

        question_counter += 1

        #query_result['results'].remove(returned_user_object_dict)



    requests_dict_to_upload = json.dumps( { "requests": requests_array } )

    # upload them
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/batch', requests_dict_to_upload, {
           "X-Parse-Application-Id": "AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ",
           "X-Parse-Master-Key": "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv",
           "Content-Type": "application/json"
         })
    creation_result = json.loads(connection.getresponse().read())
    pprint (creation_result)













