#this code(tweet1.py) extracts data from twitter and stores it in a mongo db data base
#tools used: 1>Python editor 2>Mongodb Database 3>Robo 3T..
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import urllib
import tweepy
import json
import os
from pymongo import MongoClient
 
MONGO_HOST='mongodb://localhost/info'

Ckey=os.environ.get('ckey')
Csecret=os.environ.get('csecret')
Atoken=os.environ.get('atoken')
Asecret=os.environ.get('asecret')


class listener(StreamListener):
 	def on_data(self,data):
 		try:
 			client=MongoClient(MONGO_HOST)
 			db=client.info
 			datajson=json.loads(data)
 			created_at=datajson['created_at']
 			print("Tweet collected at" + str(created_at))
 			db.information.insert(datajson)
 			

 		except Exception as e:
 			print(e)


 	def on_error(self,status):
 		print(status)


auth=OAuthHandler(Ckey, Csecret)
auth.set_access_token(Atoken, Asecret)


stream=Stream(auth,listener())
stream.filter(track=["Corona","Sushant Singh Rajput"])


