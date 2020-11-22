import kafka
from kafka import KafkaProducer
import json
import re
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener


# Twitter Api Configurations from Twitter Developer
#Registered the client application with Twitter and got the keys
consumer_key = "jlHmf3kOTKTbr0k7S0hYAAIFk"
consumer_secret = "vUdtAruIWL4IsxALrwUW59fJLg2pxSDqnZ3zH8m7yVjkUxLRx5"
access_token = "873723202467319808-vratbHA3hSi5WKSi4UHTwNL1qbR7pLM"
access_secret = "RaXxven5WBrxB6sZWuHU1waZdRI7HHgg3elok7Mh3W2zv"

# Twitter Api Authorization
#creating an OAuthHandler instance
auth = OAuthHandler(consumer_key, consumer_secret)
#set the access token
auth.set_access_token(access_token, access_secret)

#calling tweepy api using authorization
api = tweepy.API(auth)

 
# Twitter Stream Listener
class KafkaPushListener(StreamListener):
    def __init__(self):
        # Default Zookeeper Producer Host and Port Adresses (localhost:9092), constructor for producer to talk to channel, hits port 9092 
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
       

    # Get Producer that has topic name is Twitter
    #Any data received by producer is put into topic "Twitter"
    def on_data(self, data):
        # Producer produces data for consumer
        # Data comes from Twitter 
        print(data)
        self.producer.send("twitter", data.encode('utf-8'))
        print("---------------------------")
        return True

    def on_error(self, status):
        print(status)
        return True


# Configure the Twitter Stream (Part of Twitter API)
twitter_stream = Stream(auth, KafkaPushListener())

# Filter Data that has either trump or coronavirus hashtag (Tweets)
twitter_stream.filter(track=['#trump','#coronavirus'])