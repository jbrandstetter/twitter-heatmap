import tweepy
import json
from pymongo import Connection
from bson import json_util
from tweepy.utils import import_simplejson
json = import_simplejson()
import sys
import time
import os

print("connecting to MongoDB...")

mongocon = Connection()

db = mongocon.tstream
#check if exists
try:
    db.create_collection("tweets", capped=True, size=100000)
except Exception, e:
    print e
    pass

col = db.tweets



#read config from environment
consumer_key = os.environ['CONSUMERKEY']
consumer_secret =  os.environ['CONSUMERSECRET']
access_token_key =  os.environ['ACCESSTOKENKEY']
access_token_secret =  os.environ['ACCESSTOKENSECRET']


auth1 = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth1.set_access_token(access_token_key, access_token_secret)

class StreamListener(tweepy.StreamListener):
    mongocon = Connection()
    db = mongocon.tstream
    try:
        db.create_collection("tweets", capped=True, size=100000)
    except Exception, e:
        print ("in class")
        print e
        pass
    col = db.tweets
    json = import_simplejson()

    def on_limit(self, track):
        sys.stderr.write(track + "\n")
        return

    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False

    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return


    def on_status(self, tweet):
        print 'Ran on_status'


    def on_data(self, data):
        #tweet = json.loads(data,  object_hook=json_util.object_hook)
        #print "1" + json.dumps(tweet)
        #data1 = data.rsplit("\n")

        if data[0].isdigit():
            print ("kaputt data")
        else:
            decoded = json.loads(data)
            try:
                #print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
                #print decoded
                pass
            except Exception, e:
                print e
            #if coords not None
            coord_count = 1
            no_coord_count = 0
            if decoded['coordinates'] is not None:
                print ("coords there, inserting")
                print '@%s: %s %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'), decoded['coordinates'])
                coord_count+=1
                col.insert(json.loads(data))
            else:
                print ("no coords")
                no_coord_count+=1
        #print no_coord_count / coord_count
        #print(json.loads(data1))


if __name__ == '__main__':
    l = StreamListener()
    print ("starting stream")
    streamer = tweepy.Stream(auth=auth1, listener=l)
    setTerms = ['hello', 'goodbye', 'goodnight', 'good morning']
    #setTerms = ['and', 'flight', 'sotu', 'obama']
    print ("setting terms")
    print setTerms
    try:
        streamer.filter(track = setTerms)
    except Exception, e:
        print e
        print "error!"
        streamer.disconnect()
