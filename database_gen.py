from HTMLParser import HTMLParser
from os import listdir
import re

"""Module to convert html to plain text"""
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def handle_entityref(self, name):
        self.fed.append('&%s;' % name)
    def get_data(self):
        return '\n'.join(self.fed)

def html_to_text(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

"""Define Quote and Scene classes"""
class Quote:
	def __init__(self):
		self.episode = None
		self.quote = ""
		self.character = None
	def __repr__(self):
		return "Character: " + self.character + "\n" + self.quote + "\n(from " + \
			self.episode + ")\n\n"

class Scene:
	def __init__(self):
		self.setting = ""
		self.episode = None
		self.dialogue = ""
		self.characters = set()

"""Conversion module from plain text to scene/quote objects for episode"""
def plainEpConvert(transcript):
	titlefound = False
	activeScene = None
	epQuotes = []
	epScenes = []
	for line in transcript.split('\n'):
		#print "currently analyzing: " + line
		if not titlefound and not re.match(r'^\s*$', line):
			print "extracting title . . ."
			title = line
			titlefound = True
			print "Analyzing Episode:" + title
		elif "[Scene: " in line:
			if activeScene:
				epScenes.append(activeScene)
			activeScene = Scene()
			activeScene.episode = title

		
		elif ":" in line:
			print line
			q = Quote()
			q.episode = title
			print line.split(":")
			q.character,q.quote = line.split(":")
			epQuotes.append(q)

	return epQuotes, epScenes



ep = "friendsalltranscripts/0101.html"
#for ep in listdir("friendsalltranscripts/"):

htmlfile = open(ep, 'r')
transcript = html_to_text(htmlfile.read())
print transcript
htmlfile.close()

print(plainEpConvert(transcript))

