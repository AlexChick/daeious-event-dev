# EVENT_NUMBER = 98

# class Event(object):
# 	print EVENT_NUMBER, 1
# 	global EVENT_NUMBER # allows access to EVENT_NUMBER inside print_this().
# 	EVENT_NUMBER = 0
# 	print EVENT_NUMBER, 2
# 	EVENT_NUMBER += 1
# 	print EVENT_NUMBER, 3
# 	a = 0

# 	def __init__(self):
# 		Event.a += 1
# 		print Event.a
# 		self.eNum = EVENT_NUMBER

# 	def print_this(self):
# 		print self.eNum, 5
# 		print EVENT_NUMBER, 6
# 		EVENT_NUMBER += 1
# 		print EVENT_NUMBER, 7

class Event():

	global MEN
	global WOMEN
	global START_AT_ROUND
	MEN = 7
	WOMEN = 9
	START_AT_ROUND = 0

	def __init__(self, men = 20, women = 25):

		#print MEN, WOMEN, 1
		print men, women, 4
		#MEN += 1
		#print MEN, WOMEN, 2
		self.men = men
		self.women = women
		self.something = MEN
		
		#self.MEN = MEN + 2
		#self.WOMEN = WOMEN + 2
		#print self.MEN, self.WOMEN, 3

		START_AT_ROUND = 5

	def do_something(self):
		print MEN, WOMEN, 19



e = Event()
print e.men, e.something, START_AT_ROUND
