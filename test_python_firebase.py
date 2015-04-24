
from pprint import pprint
from firebase import Firebase
import requests

f = Firebase('https://burning-fire-8681.firebaseio.com/see-again-choices-R1/Alex')
r = f.push(
		{
			"user_num": 24,
			"n": 9,
			"mn": 5,
			"my": 7,
			"y": 12
		}
	)

# ff = Firebase('https://burning-fire-8681.firebaseio.com/see-again-choices-R1/{}'.format(r["name"]))
s = f.get()


print r # {u'name': u'-Jnbjgqt4tThZmXkyhcS'}
# print s # {u'name': u'-Jnbjh7LWmhSyoIGbgyZ'}
pprint(s)

pprint(s[r["name"]])

# These are the names of the snapshots -- 
# dictionaries containing Firebase's REST response.

print "\n\n\n\n"

ff = Firebase("https://burning-fire-8681.firebaseio.com/see-again-choices-R1")

ss = ff.get()

pprint (ss)