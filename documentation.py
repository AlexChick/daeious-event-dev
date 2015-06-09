





"""  R0.analyze  """
'''
It is passed a list of all event users, including ghosts. These event users are assigned semi-random values for things like:
'''
hotness # (a Round-0 / pregame desirability) — 100 = very desirable (out of 100 ppl, 100 would say “yes”)
nixness # (a Round-0 / pregame selectivity) — 0 = very selective (they would say “no” to 100 out of 100 ppl)
personality # (A random int, 0-100. If your personalities are similar, you might be somewhat more likely to choose each other.)
(?) clothing (how well you’re displaying yourself)
(?) hair color
(?) eye color
(?) height
(?) weight
(?) age
(?) education
(?) IQ
(?) number of events previously attended (experience?)
 
The code in main() is:
--------------------------------- 
r0.analyze(li_all_eu)    
---------------------------------


"""  R1.plan  """

'''
Once the event users are assigned those pregame attributes, the li_all_eu is iterated through (first by subround, then by station) and, for each station in each subround, a basic interaction object is created containing:
'''

Carried over from _Interaction:

    e # event object
    r # round object

    ix_num
    event_nm
    round_num

    meu # male and female event user objects
    feu 
    m_eu_num
    f_eu_num 

Newly created:

    sub_num
    sta_num
    q_num
    m_ipad_num
    f_ipad_num

    m_hotness
    f_hotness
    m_nixness
    f_nixness
    m_personality
    f_personality

'''These objects are put into a list of planned round-1 interactions (li_r1_ix_planned).'''

The code in main() is:
------------------------------------- 
li_r1_ix_planned = r1.plan(li_all_eu)
-------------------------------------


"""  R1.simulate  """
'''
Round 1 is played — the ix’s in li_r1_ix_planned are simulated — they occur “in real life”. For each ix in the list, at least 4 values are added, and each ix is then put into a li_r1_ix_simulated.
'''
m_sac # (male see-again choice.   0 = no;   1 = maybe-no;   2 = maybe-yes;   3 = yes  )
f_sac # (female see-again choice)
m_qa # (male question-answer, if any)
f_qu # (female question-answer, if any)
(?)  time_m_sac (time male took to choose)
(?)  time_f_sac (time female took to choose)
(?)  time_m_qa (time male took to answer question, if he answered it)
(?)  time_f_qa (time female took to answer question, if she answered it)

'''The code in main is:'''
-------------------------------------------------- 
li_r1_ix_simulated = r1.simulate(li_r1_ix_planned)
--------------------------------------------------


"""  R1.analyze  """
'''
Round-1 interactions are analyzed. Computational data are added, both to the ix objects list (li_r1_ix_simulated) and to that of the eventusers (li_all_eu).
'''
'''Each ix gets:'''

sum_sac # (the sum of the see-again choices)
agree # (boolean, whether they agreed about the question)
m_hotness # (useful for r2.plan)
f_hotness # (useful for r2.plan)
m_neediness # (useful for r2.plan)
f_neediness # (useful for r2.plan)
rank # (how much should it happen again? 1 means it was the best; 2601 was the worst. They hated each other. Complete oppos.

'''Each eu gets:'''

num_r1_rcvd_yes # (of the 51 interactions, how many ppl said “yes” to them?)
num_r1_rcvd_my
num_r1_rcvd_mn
num_r1_rcvd_no
num_r1_gave_yes # (of the 51 interactions, how many ppl did he or she say “yes” to?)
num_r1_gave_my
num_r1_gave_mn
num_r1_gave_no
num_r1_rcvd_total   
num_r1_gave_total
score_r1_sel   # (num_r1_gave_total, scaled…range is 0 to 153 (= 3 x num_r1_ix_pp), so just divide by 1.53 to achieve a range of 0-100) (what percentage of possible “points” did they give to others in the round?)
score_r1_des   # (num_r1_rcvd_total, scaled…range is 0 to 153 (= 3 x num_r1_ix_pp), so just divide by 1.53 to achieve a range of 0-100) (what percentage of possible “points” did they “earn” from others in the round?
ratio_r1_recv_decisiveness   # (ratio of how many “yes” and “no” did they received vs. how many maybes?)
ratio_r1_gave_decisiveness   # (ratio of how many “yes” and “no” did they gave vs. how many maybes?)

'''… and probably some others, but that’s enough for now.'''

'''
Put all the updated ix’s into a new list: li_r1_ix_analyzed. '''## put all the updated eu’s into a new list: li_eu_after_r1. (?? - couldn’t I just always use 1 eu list? li_eu?)
 
The call is:
-------------------------------------------------- 
li_r1_ix_analyzed = r1.analyze(li_r1_ix_simulated)
--------------------------------------------------


"""  R2.plan  """
"""
Now, Round 2 is prepared — it is decided which R1 interactions will happen again. This is a tricky process. It’s the heart of the algorithm. It can be done many different ways:
1.
Rank each r1-ix according to sum_sac first, then things like agree, score_r1_sel, score_r1_des, hotness, nixness, et cetera. Then start at interaction ranked #1 and go down the list, trying to make each interaction happen by checking to see if (a) the person already has 15 planned R2 interactions, and (b) both people have a free subround. If so, plop them into their next available subround. … This seems tricky.
2.
Make some algorithm that takes the top 13 * 51 = 663 interactions and does several random auto-placements of them into the 663 slots, keeping the best (defined as placing the most, or the highest inverse-value sum of ix_num) after each new try, and trying for as many times as is practical before stopping. When it stops, take the number it couldn’t place and go through the rest of the list (#664, #665, etc) and try to place that many, stopping when no more can be placed. … This could work. It could also give an optimal solution for the 663 best ix’s, and then be unable to completely fill the event. You don’t want any interactions happening again where either person said “no”. Maybe those should be thrown out. And maybe every auto-placement attempt of the first 663 should include placement of the rest, and only then could it be considered valid. Goes through entire list only once. (+)
    --  It looks like, since the womens' stations are essentially fixed (b/c they can only move one station right), there's only one unique outcome achieved by iterating through the list of the highest-ranked interactions, no matter where the women start. Which makes sense.
    --  The question now becomes: is this the best, and can I fill in the un-filled subround stations, either efficiently or at all? I'm going to try to fill them in.
    --  The best way to do this is to try to fill in all the (3,3)'s, then all the (3,2)'s, and so on, ...
    --  Try to give everyone 12 r2ix's, then add a 13th if necessary for people already with 12 to get everyone under 12 up to 12.
    --  The best way to do this is to try to fill in all the (3,3)'s, then all the (3,2)'s, and so on, to get people up to 12, and then do it again, to get people under 12 up to 12.

3.
Only make one subround’s ix’s at a time. Iterate through the (2,600-member) list once for each subround, trying to give each person a pairing for that subround. This is possible, but might be slow, and could result in several low-quality interactions happening again.

--- I won’t know which is best until I test them...that’s the whole point of why I’ve been doing this. So just keep thinking of different ways it might be done, and I can test them.

--- No matter how the algorithm functions, it returns a new list of 51 * 13 = 663 new ix objects called li_r2_ix_planned, with each ix containing:
"""
    ix_num
    sub_num
    sta_num
    q_num
    m_ipad_num, f_ipad_num
    m_eu_num, f_eu_num 
    m_r1_sac, f_r1_sac
    m_hotness, f_hotness
    m_nixness, f_nixness
    m_personality, f_personality
    m_r1_des, f_r1_des
    m_r1_sel, f_r1_sel

The code in main is:
---------------------------------------------
li_r2_ix_planned = r2.plan(li_r1_ix_by_energy)        
---------------------------------------------


"""  R2.simulate  """
Round 2 is played — the ix’s in li_r2_ix_planned are simulated — they occur “in real life”. For each ix in the list, at least 4 values are added, and each ix is then put into a li_r2_ix_simulated.
This is mostly the same as STEP 3, but the weighted randomization of their sac’s is slightly different.
    m_sac # (male see-again choice.   0 = no;   1 = maybe-no;   2 = maybe-yes;   3 = yes  )
    f_sac # (female see-again choice)
    m_qa # (male question-answer, if any)
    f_qu # (female question-answer, if any)
  

The code in main is:  
--------------------------------------------------
li_r2_ix_simulated = r2.simulate(li_r2_ix_planned) 
--------------------------------------------------


"""  R2.analyze  """

For now, same analysis as in R1.analyze. Might incorporate r1_sac_total, and/or some other things.

The code in main is:  
--------------------------------------------------
li_r2_ix_analyzed = r2.analyze(li_r2_ix_simulated) 
--------------------------------------------------


"""  R3.plan  """
Similar to R1.plan and R2.plan. No matter how the algorithm functions, it returns a new list of 51 * 5 = 255 new ix objects called li_r3_ix_planned, with each ix containing:
    ix_num
    sub_num
    sta_num
    q_num
    m_ipad_num, f_ipad_num
    m_eu_num, f_eu_num
    m_r1_sac, f_r1_sac
    m_r2_sac, f_r2_sac
    m_hotness, f_hotness
    m_nixness, f_nixness
    m_personality, f_personality
    m_r1_des, f_r1_des
    m_r2_des, f_r2_des
    m_r1_sel, f_r1_sel
    m_r2_sel, f_r2_sel


  
The code in main is: 
---------------------------------------------
li_r2_ix_planned = r2.plan(li_r1_ix_analyzed)
---------------------------------------------


"""  R3.simulate  """

Similar to R1 and R2, but the final choice is whether to go out sometime. In real life, this is left up to the people, and no record is kept. The third round is really just for getting to know your “Final 5” a little bit better before you exchange contact info or connect over Facebook. It’d be nice to have a record of how many people are exchanging contact info…perhaps there can be options to connect over Facebook, or give your phone number, or set up a date, and it’s up to the pair to decide what they want to do. Whatever they choose, they both have to choose it for it to happen. This would be an excellent time for implementing my idea about making a button you press on your iPad change the color of the same button on your partner’s iPad to show them your selection, and then something “clicks” or whatever if / when your partner presses the same button.
















