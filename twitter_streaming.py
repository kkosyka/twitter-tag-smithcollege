# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '28930526-ttro9V7TUvuUfXMe4e3OBMlU38MuKn9ISLUwqMvP9'
ACCESS_SECRET = 'dI0t4RRSJU53FciGw1jYfApDkx1x3znrWwH9zSdfetQjh'
CONSUMER_KEY = '3KUdtFeceeLB3rs3pJDe4fbeM'
CONSUMER_SECRET = 'vPps0BgF2Vm0UZXKdi67URWUnIl5ygk1m5KLRHbXVWwGHCoej1'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)
twitter = Twitter(auth=oauth)

#Creates new file that will contain the most 30 recent tweets that contain #smithcollege
newFile = "TAGsmithcollegeInTweet.txt" #example file
newFile = open(newFile, 'w')
newFile.write(str(twitter.search.tweets(q='#smithcollege', result_type='recent', lang='en', count=30)))
