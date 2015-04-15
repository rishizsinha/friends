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
	title = transcroup.title.string.encode("utf8")
	text = transcroup.get_text()
	activeScene = None
	activeQuote = None
	epQuotes = []
	epScenes = []
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
					activeScene.dialogue += activeQuote.character + ":" + \
						activeQuote.quote + "\n"
			activeQuote = Quote()
			activeQuote.episode = title
			activeQuote.character,activeQuote.quote = line.split(":", 1)
		else:
			if activeQuote:
				activeQuote.quote += " " + line
				if activeScene and activeQuote.character not in activeScene.characters:
					activeScene.characters.append(activeQuote.character)
	return json.dumps(epQuotes), json.dumps(epScenes)

def main():
	allquotes = []
	allscenes = []
	BASE = "friendsalltranscripts/"
	for ep in listdir(BASE):
		print ep
		f = open(BASE+ep, 'r')
		soup = BeautifulSoup(f)
		res = epConvert(soup)
		allquotes.append(res[0])
		allscenes.append(res[1])

	qdb = open("quotedb.json", 'w')
	sdb = open("scenedb.json", 'w')
	qdb.write(json.dumps(allquotes))
	sdb.write(json.dumps(allscenes))
	qdb.close()
	sdb.close()
	
main()

"""
ep = open("friendsalltranscripts/0101.html",'r')
soup = BeautifulSoup(ep)
print(epConvert(soup))
"""



