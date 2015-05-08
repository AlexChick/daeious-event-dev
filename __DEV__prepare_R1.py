"""
"""



def prepare_R1(m, f, mg, fg, s):
	"""
	males, females, ghosts, stations

	Create Round-1 Interactions.

	For now, station Nums, iPad Nums, etc. start at 1, 2, 3, ...,
	but that will be changed so that the correct Nums are chosen 
	and put into lists.

	(It's tricky to do these random simulations because to make it realistic
		I'd have to pull only those objects with array_eventsRegistered 
		containing the eNum. To truly randomize things, I guess I could
		create an event with a random number of men and women every time...
		and while that seems like it's a lot more work, it also seems beneficial
		in the long run -- testing will be easier, and the DEV program will
		be closer to the real thing. There's NO reason to rush into getting
		some kind of version of this completed...I've built a version before,
		so I already know I can do it. Now I just need to do it really well.
	"""

	i = s * 2

	s_nums = list(x+1 for x in range(s))
	i_nums = list(x+1 for x in range(i))

