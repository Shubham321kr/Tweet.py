from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import urllib
class listener(StreamListener):
	def on_data(self,data):
		file=open("twitter.json","a")
		file.write(data + "\n")
		file.close()
		print("Record Saved")
		return(True)
	def on_error(self,status):
		print(status)

auth=OAuthHandler("ID2FRiuZOVfRLQLEdl1zdfRKj","Yvp5EdzewX7J2TtX71Sb5ucrF98M52aFI7c9HiRysY0hgUW8DL")
auth.set_access_token("124726061-4cg94in8BVYPnTx8jh3uZGiNEinN2UHOq8q5bKVf","Ja2Umx43XLXNVDKTyJEciKTHAwONS9ohJ7mdy3MxXl5mK")

stream=Stream(auth,listener())
stream.filter(track=["Corona","Sushant Singh Rajput"])
