#To run this install these modules:tweepy,textblob,NLTK corpora
#Here we are extracting data from twitter and doing sentiment analysis and store data in mongodb database

import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob
import os 
from tweepy import Stream
from tweepy.streaming import StreamListener
import urllib
import json
from pymongo import MongoClient
#To run this install these modules:tweepy,textblob,NLTK corpora
#Here we are extracting data from twitter and doing sentiment analysis
import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob
import os 
MONGO_HOST='mongodb://localhost/info'

Ckey=os.environ.get('ckey')
Csecret=os.environ.get('csecret')
Atoken=os.environ.get('atoken')
Asecret=os.environ.get('asecret')

#---------------------

class TwitterClient(object): 
	
	def __init__(self): 
		
		consumer_key = os.environ.get('ckey')
		consumer_secret = os.environ.get('csecret')
		access_token = os.environ.get('atoken')
		access_token_secret = os.environ.get('asecret')


		try: 
			
			self.auth = OAuthHandler(consumer_key, consumer_secret) 
			 
			self.auth.set_access_token(access_token, access_token_secret) 
			
			self.api = tweepy.API(self.auth) 
		except: 
			print("Error: Authentication Failed") 

	def clean_tweet(self, tweet): 
		
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 

	def get_tweet_sentiment(self, tweet): 

		analysis = TextBlob(self.clean_tweet(tweet)) 
		
		if analysis.sentiment.polarity > 0: 
			return 'positive'
		elif analysis.sentiment.polarity == 0: 
			return 'neutral'
		else: 
			return 'negative'

	def get_tweets(self, query, count = 10): 
		
		tweets = [] 

		try: 
		
			fetched_tweets = self.api.search(q = query, count = count) 

		
			for tweet in fetched_tweets: 
				
				parsed_tweet = {} 
 
				parsed_tweet['text'] = tweet.text 
				
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

				
				if tweet.retweet_count > 0: 
			
					if parsed_tweet not in tweets: 
						tweets.append(parsed_tweet) 
				else: 
					tweets.append(parsed_tweet) 

		
			return tweets 

		except tweepy.TweepError as e: 
			
			print("Error : " + str(e)) 

def main(): 
	
	api = TwitterClient() 
	
	tweets = api.get_tweets(query = 'Sushant Singh Rajput', count = 200) 

	
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
	
	print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
	

	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
	
	print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
	
	 
	print("Neutral tweets percentage: {} % ".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)))

	


	 
	print("\n\nPositive tweets:") 
	for tweet in ptweets[:10]: 
		print(tweet['text']) 

	
	print("\n\nNegative tweets:") 
	for tweet in ntweets[:10]: 
		print(tweet['text']) 

if __name__ == "__main__": 
	
	main() 
#--------------------------
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
stream.filter(track=["Sushant Singh Rajput"])
