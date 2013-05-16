import sys
import time
import config
import time
import praw
from GildedComment import GildedComment

# haven't done python in centuries, so this will be interesting ;)
r = praw.Reddit(user_agent = 'User-Agent: Bot that looks through gilded comments, finds comments above 3 gilds, and then submits them to r/' + config.subreddit + ', by /u/macromaniac')

submittedDict = {}

def getStr( thing ):
	return str(thing.gilded) + ' ' + thing.subreddit.display_name + ' ' + str(thing.author.name) + ' ' +  thing.id + ' ' + str(thing.created_utc) + ' '

def getDay():
	return time.strftime('%Y-%m-%d', time.localtime())

def submitLink( gildedComment ):
	#the dictionary is a crude protection against reposts. If the program gets restarted it will try
	#to resubmit all the links for the day and then fail. Not a big deal. An easy improvement would be
	#to use persistant data
	if !(gildedComment.getID in submittedDict):
		submittedDict[gildedComment.getID] = 1
		try:
			print('trying to submit to r/' + str(config.subreddit) + ' title: ' + str(gildedComment.getTitle()) + ' url: ' + str(gildedComment.getPerma()))
			r.submit( config.subreddit, gildedComment.getTitle() , url = gildedComment.getPerma()  )
			print("submitted link!")
		except praw.errors.AlreadySubmitted:
			#if they comment was already submitted, ignore it
			pass
		except praw.errors.NotLoggedIn:
			print("Bot got logged off!")
			sys.exit(1)

def parseComments():
	comments = r.get_comments('all', gilded_only = True, limit = None)
	already_done = []
	for comment in comments:
		if comment.gilded >= config.threshold:
			#get the gilded comment
			gildedComment = GildedComment(comment)
			#if the comment was posted today try to submit it
			if( gildedComment.getDay() == getDay() ):
				submitLink(gildedComment)

def mainLoop():
	while True:
		parseComments()
		time.sleep(config.pollrate)

def init():
	print('Starting Bot...')
	try:
		r.login( config.username, config.password)
	except praw.errors.NotLoggedIn:
		print("Bot couldn't log in, exiting")
		sys.exit(1)
	print('Bot logged in, Parsing comments...')
	mainLoop()

init()
