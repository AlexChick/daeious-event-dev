
# https://www.random.org/strings/?mode=advanced

iPadSerialNumbers_list = [
"lo4cWpEOhzbGEZj2",
"FXoRIsHIu8qv911S",
"IzArOMhwALYjxGpz",
"1AmmS6O3saDNREtv",
"V9HLmGjEHFu9Ka31",
"piZ2egrZ66ncEEGn",
"BrasV9S6oTF5JbWm",
"HUEowznvmBZT11Ed",
"ce83Fkaxy08u61GO",
"Hjnd9NqQw1ZE1Q45",
"l892lbPjg9hjm4dA",
"YwztD66NM23MgYPJ",
"Q4Nd6Yaxd4GiMD3N",
"IkyNhuh6zsrayeNH",
"rWpTkM2JeFDi0IK8",
"AfIKw15rPBnINEXj",
"E1GaWX3tqTXMH9gX",
"6Oqg9FWE4iuJmuaW",
"8TAu672Oebrw4zEC",
"l8fnpYtnz4JySsqC",
"jBZmL7raspgUkros",
"uOSMfiq7au4DdIJG",
"8grHBy4gfJZH7XRs",
"gGSDW1bafVJE5dvs",
"JFt08pmdJ6CUYWR3",
"LFTBCtnnJud3umna",
"guEDaHl3ebruyYS8",
"8wG1XZ8wJfr8MhF4",
"CcwyqfWYWAYWQi77",
"4cDdp4lnk98eSxc5",
"foF6NlvzTKXILezS",
"weeDpuix3i5tan1q",
"3sQWepXBbXDd041c",
"9jxhKyjBqZs7C4YP",
"xYSgGDoljb1lHau6",
"eIFHMi3cAVdY6aNb",
"r7JlA5RKYJapESiN",
"xbA1pqc71bktm4fp",
"kS8Tczm1ujg2Aini",
"QmRqJz9ZcIMRh13L",
"RVGayiLEK8RQU234",
"hQhPJTlxFFxCoAyW",
"LGK1SXTPVQBO9Xi0",
"Opo3njWOLVnTcQWA",
"3qChnouLXg1tVGVS",
"uAjxkAFitWCOXsua",
"WTZNg9pboZKtOx1N",
"9j5wI7ridCWoSxco",
"qOuVdJZU1y8VCFpD",
"IA4M2DZacErK95pz",
"53SokH1ae3KPgKOC",
"wNIDVrWV6mRkRGWT",
"sXXuSMJ5cpgjZrba",
"wnJnZJWiXnRVyPZV",
"Icfqf9JBY2VamVXn",
"75h4DpX2sFRgW45z",
"Sh8opOezgfx84jTy",
"TxyyRQyGce618mtM",
"CRGMMhXTiYHcdjBo",
"vDKbwVyE5takLRfq",
"Q7GobNPOXKj0Hy7A",
"kFg7vjIVGpN1anJY",
"nTFEMNGWp1t0Mbjw",
"wj17Swy03WG3yxHw",
"fJzRUSObkOzKSERe",
"eBhtdlU78gFOOlps",
"P9JADxyceqPDpBDn",
"XC8FVHksgd0lhjkz",
"gAEzkVCYKlKf5fDi",
"r6ycRkjmG6fILuBi",
"lP6vP3DTMXWbMAWA",
"IMeBKANoXsXr6Rqh",
"y5g6jxmojP3T26Nf",
"gu8tiCeL8EhgZ78s",
"fC4ZnAG9sQREf2Wu",
"ao57Myjs4teGf5dx",
"4UiMCsVW78AeYfIp",
"0nM5lCTphUxRv7hm",
"nK3w0uMS2bWt3D73",
"vOZHkug5tp5edtCx",
"Sqxbun9Kb3wL1dIr",
"xRZyozq4V3lmjG3V",
"ABjt9KLICzTnl9tT",
"geYuG0p6gPi0hkgK",
"QkyEDnvlvPo18JtJ",
"0NcwixRjgpncylYP",
"atPqDvRkLgqgmR1O",
"vhPSFnM6mmHB1eAz",
"ybaVNO2tdt6DnDuj",
"opK8y4igSdso5sBU",
"W3Q9VY3Ts5Lsg2QF",
"586f3McsyKcx3MsU",
"bpn0qalUK0xhATDi",
"F7cOpm9ikpIn7HUx",
"fyfHylqm8UAIr7p0",
"ZJyvYLQQTxFrQNmx",
"QRTccCF8ILAcvVOF",
"B3mg6BgQKKAPXHlb",
"Tk3RoZUL4BAecfhs",
"miC1swkZhq7OvbZJ"
]

iPadCreator = open("100_iPads.json", "w")

iPadCreator.write("{ \"results\": [\n\n")

for i in range (len(iPadSerialNumbers_list)):
	firstPart = "    {\n        \"iPad_Id\": %d,\n" % (i+1)
	iPadCreator.write(firstPart)
	if i != 99:
		iPadCreator.write("        \"iPadSerialNumber\": \"" + iPadSerialNumbers_list[i-1] + "\"\n    },\n\n")
	else:
		iPadCreator.write("        \"iPadSerialNumber\": \"" + iPadSerialNumbers_list[i-1] + "\"\n    }\n\n")

iPadCreator.write("]}")
iPadCreator.close()






















