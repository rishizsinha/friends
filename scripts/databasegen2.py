from os import listdir
from bs4 import BeautifulSoup
import re
import json




"""Define Quote and Scene classes"""
class Quote:
	def __init__(self):
		self.episode = None
		self.quote = ""
		self.character = None
	def __repr__(self):
		return "Character: " + self.character + "\n" + self.quote + "\n(from " + \
			self.episode + ")\n\n"
	def tojson(self):
		return {"character":self.character, "quote":self.quote, \
			"episode":self.episode}

class Scene:
	def __init__(self):
		self.setting = ""
		self.episode = None
		self.dialogue = ""
		self.characters = []
	def __repr__(self):
		return self.setting + "\nCharacters: " + \
			repr(self.characters) + "\n" + self.dialogue + "\n(from " + \
			self.episode + ")\n\n"
	def tojson(self):
		return {"setting":self.setting, "characters": self.characters, \
			"dialogue":self.dialogue, "episode":self.episode}

def epConvert(transcroup):
	title = transcroup.title.string
	text = transcroup.get_text()
	activeScene = None
	activeQuote = None
	epQuotes = []
	epScenes = []
	epChars = set()
	for line in text.splitlines():
		line = line.encode("utf8")
		if "[Scene: " in line:
			if activeScene:
				epScenes.append(activeScene.tojson())
			activeScene = Scene()
			activeScene.episode = title
			activeScene.setting = line[1:]
		elif re.match("^\w+:",line):
			if activeQuote:
				epQuotes.append(activeQuote.tojson())
				if activeScene:
					activeScene.dialogue += activeQuote.character + ": " + \
						activeQuote.quote + "\n"
			activeQuote = Quote()
			activeQuote.episode = title
			qsplit = line.split(":", 1)
			activeQuote.character = qsplit[0].title()
			epChars.add(activeQuote.character)
			activeQuote.quote = qsplit[1]
		else:
			if activeQuote:
				activeQuote.quote += " " + line
				if activeScene and activeQuote.character not in activeScene.characters:
					activeScene.characters.append(activeQuote.character)
	#print title, list(epChars)
	return epQuotes, epScenes, epChars, title

def main():
	allquotes = []
	allscenes = []
	characters = set()
	eps = []
	BASE = "../rawtranscripts/"
	for ep in listdir(BASE):
		print ep
		f = open(BASE+ep, 'r')
		soup = BeautifulSoup(f)
		res = epConvert(soup)
		allquotes += res[0]
		allscenes += res[1]
		characters = characters.union(res[2])
		eps.append(res[3])
	print eps
	print characters
	qdb = open("../data/quotedb.json", 'w')
	sdb = open("../data/scenedb.json", 'w')
	cdb = open("../data/chardb.json", 'w')
	epdb = open("../data/epdb.json", 'w')
	qdb.write(json.dumps(allquotes))
	sdb.write(json.dumps(allscenes))
	cdb.write(json.dumps(list(characters)))
	epdb.write(json.dumps(eps))
	qdb.close()
	sdb.close()
	cdb.close()
	epdb.close()

main()

"""
ep = open("friendsalltranscripts/0101.html",'r')
soup = BeautifulSoup(ep)
print(epConvert(soup))
"""



