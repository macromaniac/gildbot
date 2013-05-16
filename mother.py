import time
import config
import time
import praw
from GildedComment import GildedComment

# haven't done python in centuries, so this will be interesting ;)
r = praw.Reddit(user_agent = 'Bot that looks through gilded comments, finds comments above 3 gilds, and then submits them to r/' + subreddit + ', code @ https://github.com/macromaniac/gildbot')

def getStr( thing ):
	return str(thing.gilded) + ' ' + thing.subreddit.display_name + ' ' + str(thing.author.name) + ' ' +  thing.id + ' ' + str(thing.created_utc) + ' '

def getDay():
	return time.strftime('%Y-%m-%d', time.localtime())

def submitLink( gildedComment ):
	try:
		r.submit( config.subreddit, gildedComment.getTitle() , url = gildedComment.getPerma()  )
		print("submitted link!")
	except praw.errors.AlreadySubmitted:
		#if they comment was already submitted, ignore it
		pass

def parseComments():
	comments = r.get_comments('all', gilded_only = True, limit = None)
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
		time.sleep(pollrate)

def init():
	print('Starting Bot...')
	r.login( config.username, config.password)
	print('Bot logged in, Parsing comments...')
	print('today is: ' + str(getDay()))
	mainLoop()

init()
