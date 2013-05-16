from datetime import datetime
import time

class GildedComment:
	def __init__(self, data):
		self.gilded = data.gilded
		self.sub = data.subreddit.display_name
		self.author = data.author.name
		self.myId = data.id
		self.timeMade = data.created_utc
		self.perma = data.permalink
	def getID(self):
		return self.myID
	def getAge(self):
		return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.timeMade))
	def getDay(self):
		return time.strftime('%Y-%m-%d', time.localtime(self.timeMade))
	def getAgeSeconds(self):
		print( time.mktime(time.gmtime()))
		return time.mktime(time.gmtime()) - self.timeMade
	def getPerma(self):
		return self.perma + '?context=1337'
	def getAgeHours(self):
		return str( int( round( self.getAgeSeconds() / (60 * 60 ) ) ) )
	def getTitle(self):
		return str(self.getAgeHours()) + 'h - in r/' +  self.sub + ' by u/' + self.author
		
