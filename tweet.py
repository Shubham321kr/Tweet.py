#This code describes (Tweet.py) how we could extract tweets from twitter and store it in a File (twitter.json).
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import urllib
import os

Ckey=os.environ.get('ckey')
Csecret=os.environ.get('csecret')
Atoken=os.environ.get('atoken')
Asecret=os.environ.get('asecret')

class listener(StreamListener):
	def on_data(self,data):
		file=open("twitter.json","a")
		file.write(data + "\n")
		file.close()
		print("Record Saved")
		return(True)
	def on_error(self,status):
		print(status)

auth=OAuthHandler(Ckey, Csecret)
auth.set_access_token(Atoken, Asecret)

stream=Stream(auth,listener())
stream.filter(track=["Corona","Sushant Singh Rajput"])
