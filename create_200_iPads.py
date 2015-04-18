"""

Creates 200 iPad objects and uploads them to Parse with ParsePy.

"""

# import stuff
import itertools, math, os, random, time # python stuff
import json, httplib, urllib # parse stuff
from pprint import pprint # pretty printing
# import ParsePy stuff
from parse_rest.connection import ParseBatcher, register, SessionToken
from parse_rest.datatypes import ACL, Function, Object
from parse_rest.role import Role
from parse_rest.user import User

program_start_time = time.time()

# Calling "register" allows parse_rest / ParsePy to work.
# - register(APPLICATION_ID, REST_API_KEY, optional MASTER_KEY)
register("AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS", master_key = "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv")

# We must subclass Object for the class names we want to use
class IPad(Object):
    pass

# 200 16-character serial number strings from 
# https://www.random.org/strings/?mode=advanced
iPadSerialNumbers_list = [
"lo4cWpEOhzbGEZj2","FXoRIsHIu8qv911S","IzArOMhwALYjxGpz","1AmmS6O3saDNREtv",
"V9HLmGjEHFu9Ka31","piZ2egrZ66ncEEGn","BrasV9S6oTF5JbWm","HUEowznvmBZT11Ed",
"ce83Fkaxy08u61GO","Hjnd9NqQw1ZE1Q45","l892lbPjg9hjm4dA","YwztD66NM23MgYPJ",
"Q4Nd6Yaxd4GiMD3N","IkyNhuh6zsrayeNH","rWpTkM2JeFDi0IK8","AfIKw15rPBnINEXj",
"E1GaWX3tqTXMH9gX","6Oqg9FWE4iuJmuaW","8TAu672Oebrw4zEC","l8fnpYtnz4JySsqC",
"jBZmL7raspgUkros","uOSMfiq7au4DdIJG","8grHBy4gfJZH7XRs","gGSDW1bafVJE5dvs",
"JFt08pmdJ6CUYWR3","LFTBCtnnJud3umna","guEDaHl3ebruyYS8","8wG1XZ8wJfr8MhF4",
"CcwyqfWYWAYWQi77","4cDdp4lnk98eSxc5","foF6NlvzTKXILezS","weeDpuix3i5tan1q",
"3sQWepXBbXDd041c","9jxhKyjBqZs7C4YP","xYSgGDoljb1lHau6","eIFHMi3cAVdY6aNb",
"r7JlA5RKYJapESiN","xbA1pqc71bktm4fp","kS8Tczm1ujg2Aini","QmRqJz9ZcIMRh13L",
"RVGayiLEK8RQU234","hQhPJTlxFFxCoAyW","LGK1SXTPVQBO9Xi0","Opo3njWOLVnTcQWA",
"3qChnouLXg1tVGVS","uAjxkAFitWCOXsua","WTZNg9pboZKtOx1N","9j5wI7ridCWoSxco",
"qOuVdJZU1y8VCFpD","IA4M2DZacErK95pz","53SokH1ae3KPgKOC","wNIDVrWV6mRkRGWT",
"sXXuSMJ5cpgjZrba","wnJnZJWiXnRVyPZV","Icfqf9JBY2VamVXn","75h4DpX2sFRgW45z",
"Sh8opOezgfx84jTy","TxyyRQyGce618mtM","CRGMMhXTiYHcdjBo","vDKbwVyE5takLRfq",
"Q7GobNPOXKj0Hy7A","kFg7vjIVGpN1anJY","nTFEMNGWp1t0Mbjw","wj17Swy03WG3yxHw",
"fJzRUSObkOzKSERe","eBhtdlU78gFOOlps","P9JADxyceqPDpBDn","XC8FVHksgd0lhjkz",
"gAEzkVCYKlKf5fDi","r6ycRkjmG6fILuBi","lP6vP3DTMXWbMAWA","IMeBKANoXsXr6Rqh",
"y5g6jxmojP3T26Nf","gu8tiCeL8EhgZ78s","fC4ZnAG9sQREf2Wu","ao57Myjs4teGf5dx",
"4UiMCsVW78AeYfIp","0nM5lCTphUxRv7hm","nK3w0uMS2bWt3D73","vOZHkug5tp5edtCx",
"Sqxbun9Kb3wL1dIr","xRZyozq4V3lmjG3V","ABjt9KLICzTnl9tT","geYuG0p6gPi0hkgK",
"QkyEDnvlvPo18JtJ","0NcwixRjgpncylYP","atPqDvRkLgqgmR1O","vhPSFnM6mmHB1eAz",
"ybaVNO2tdt6DnDuj","opK8y4igSdso5sBU","W3Q9VY3Ts5Lsg2QF","586f3McsyKcx3MsU",
"bpn0qalUK0xhATDi","F7cOpm9ikpIn7HUx","fyfHylqm8UAIr7p0","ZJyvYLQQTxFrQNmx",
"QRTccCF8ILAcvVOF","B3mg6BgQKKAPXHlb","Tk3RoZUL4BAecfhs","miC1swkZhq7OvbZJ",
"MkEqpVzy34yWlBJa","SMarbQQ37V2l9Ljj","EgyjifPyEWtMEFkp","FUJLksq7aNI7HgLG",
"nBkBJU3ptfXkEesy","zIAER0B18lt54or6","9szTFdoWbVmPW3No","cQ00Cg8LzZre7K30",
"iEQMV2YuPIi9AUqy","00IXoPcZlsA8HYVm","yu7hxhFwLpKQd8KH","mmlmXj92uhcKA6WT",
"qCu82YjNVuoTUvEJ","BBQtpjRSXpp9amGk","69QOFK9D6YtwDaMc","sCWeScKGTRBG8mVo",
"VIiZ2mE9guhzITb9","tm7RIXP0hExBmmDo","frHCkN3KYGC31XDN","foeAP9CrGBz7O0sC",
"CLSZ9Zj9CfETJilr","VwPHR0DChxengXUq","cA4mRuqWtiu8OaOa","GL4nYh4cyyowLu5s",
"22s5xSaWGNyK3AsA","dspyAE1inhwyR1Hl","8oLO5IB8WRH3KTUG","aTui2qnLbUVktJmv",
"WFvVg3hYWcRfNuFK","akskl1ZtG3FOu600","sgWyDOUZQzBtIBiW","3j3vqUeOelqhMvFz",
"l8rTdHc7LBhUnL7o","IOjAhknWUSC8isND","2CE0NVDDlqhtO4PM","y7unu4oWy4Xe6Fu8",
"Igqsx14zdMnOMKQj","hrCKL0H1YlBgWMle","uZHrqmRPWpbdgU5k","zbaYp3T16sQndiwS",
"DHr6ptqIQ4G7x9Mp","PLz7WYCddPXJ5dSv","I9HHpfcxtGbbAwWa","5mRE9mRvkQU8lMnU",
"If22AQv4PVbHLXEY","36nLrnmAPvl1ADML","2tOZXSLmyvuNRkKP","lSQcOf20OFM0QNmN",
"VLyd6rC80cV3pKby","tueyNbOMBYT6alRi","tK04eVuOTnWV1q36","4aOsNdbJtDaR4xK0",
"sA8xyMh59HXjvTzg","J8o2hU4qewLqFycV","1jCQUm82pX2uUOPK","ObzvL9c59LujEjSv",
"4HLM4czp59E4P5BT","E3622Vp9fwy6Ek9C","2NrmK7IT5bzZ2Gr8","ozJhUiTWR7AofqiN",
"QPL85NXFh9J1kkYU","310UniBDNUafEgS8","F90ZaVTi3zdrZcJt","ex55NMzX0oIkc2jA",
"tXDYz9EIx9OaT4HF","drZoOCSEzsNOtfS2","p4ZNmysNULWaWC9S","ygW65DBkZwgFMliT",
"MTfc1j2KWVbywo4B","kvSchwpq6205AMzz","9XrJmjnRV8aKah4z","fRdLQgt3tdt1YNq0",
"RgoY4hXWdLMtxleT","AeD8osE8PDlrKn8Q","wJCWzLmPPTZFGOIG","JYMTrSa3sbdlE9Yq",
"zy7F7iWBaa5Xq7FH","0puYHzdHMgjP63Wf","zXSJvemK6zsrE6Vo","1GXDGqytrRkwPatf",
"GSyUycWwroCKj0IH","bcKJ62pRrgj9SXw3","ZhbnzVSWqJ6RHk26","gflObWISMQjoo8WB",
"oZ7owfjMv27Oqqzi","Arjsfswy08joCXAc","HziSwv3o9af1MWlj","c4j0jSQIeWJ7WiSh",
"i0RXjSRBUH1tAJUY","WZZKYpI3ODGPDpEP","wYDZGdlBYVcajSj1","e2CgmXzWqc5yAQRj",
"cQofDpkyna4rdxdt","zUoaZ6azzUwsScdh","u1X6swFU2glNjxhG","qXNiREjbaW4mfd43",
"EtZhT3uvBejFZqpb","eCqnRjl8dDZJTrM4","qKFbtTONxkpe3aY9","Ed8OjAH2z8Nd2R6x"
]

list_iPads_to_upload = []

# create new iPad objects, put them into a list
for index, serial_number in enumerate(iPadSerialNumbers_list):
	
	new_iPad = IPad(
		iPadNum = index + 1,
		iPadSerialNumber = serial_number,
		purchaseDate = time.strftime("%Y/%m/%d")
		)

	list_iPads_to_upload.append(new_iPad)

# upload the list of new iPad objects to Parse
batcher = ParseBatcher()
batcher.batch_save(list_iPads_to_upload[:50])
batcher.batch_save(list_iPads_to_upload[50:100])
batcher.batch_save(list_iPads_to_upload[100:150])
batcher.batch_save(list_iPads_to_upload[150:200])


print "\n\n Program finished. Time taken: {} seconds.\n\n".format(time.time() - program_start_time)




"""

Time Test Results:




"""










################

""" Old Code """

# iPadCreator = open("100_iPads.json", "w")

# iPadCreator.write("{ \"results\": [\n\n")

# for i in range (len(iPadSerialNumbers_list)):
# 	firstPart = "    {\n        \"iPad_Id\": %d,\n" % (i+1)
# 	iPadCreator.write(firstPart)
# 	if i != 99:
# 		iPadCreator.write("        \"iPadSerialNumber\": \"" + iPadSerialNumbers_list[i-1] + "\"\n    },\n\n")
# 	else:
# 		iPadCreator.write("        \"iPadSerialNumber\": \"" + iPadSerialNumbers_list[i-1] + "\"\n    }\n\n")

# iPadCreator.write("]}")
# iPadCreator.close()





















