#!/bin/env python
# encoding: utf-8

"""
Webservice prototype for exposing cell data via
HTTP and JSON/JSONP
"""


DB = 'tstream'
CELLS_COLLECTION = 'tweets'


import json
import time
import math
import redis
import threading
import signal
import sys
from flask import Flask
from flask import request
from flask import abort
from flask import url_for
from flask import make_response
from flask import Response
from pymongo import Connection
from bson import json_util
from threading import Thread


red = redis.StrictRedis()

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    sys.exit(0)

def tail_mongo_thread():
    print "beginning to tail..."
    db = Connection().tstream
    coll = db.tweets
    cursor = coll.find({"coordinates.type" : "Point" }, {"coordinates" :1},tailable=True,timeout=False)
    ci=0
    while cursor.alive:
        try:
            doc = cursor.next()
            ci += 1
            print ci
            print doc
            red.publish('chat', u'%s' % json.dumps(doc,default=json_util.default))
        except StopIteration:
            #print ("stop")
            time.sleep(1)

   

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    tail_mongo_thread() 
