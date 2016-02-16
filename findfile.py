import re
import os
import pprint

#Ricerca file all'interno di una directory
#  pattern = parte di testo da cercare nei nomifile
#  path = directory dove cercare

def findfile(pattern,path):
	result = []
	for root, dirs, files in os.walk(path):
		for name in files:
			if re.search(pattern,name,re.IGNORECASE):
				result.append(name)
	return result


pprint.pprint(findfile("py","."))
