#!/usr/bin/env python
"""
    Twitter Bot for posting craigslist postings of Free Stuff
    Python 3
    MIT License
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
    
    Fenimore Love

"""
#TODO: Fix titles before posting

import re, sys, os, time, urllib.error, urllib.request
from datetime import datetime
from time import gmtime, strftime, sleep

import tweepy
from stuffify import Stuffify
from shortenurl import make_tiny
from secrets import *

# ====== Individual bot configuration ==========================
bot_username = 'FreeStuffNY'
logfile_username = bot_username + ".log"
# ==============================================================

# Some variables, why not
NO_IMAGE = 'http://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'
FILE = 'freestuff-bot/tmp/tmp-filename.jpg'


def check_length(tweet, post):
    """Check if tweet is proper length
    
    TODO: Twitter has recently changed how it counts characters.
    """
    if len(tweet) < 145: # tweet is good
        return tweet
    else:
        log("Tweet too long")
        tweet = post["loc"] + "\n" + post["title"] + " " + post["url"] 
        if len(tweet) > 144: # tweet is still not good 
            tweet = post["title"] + " " + post["url"]
            return tweet
        return tweet


def create_tweet(stuff):
    """Create string for tweet with stuff."""
    post = {"title": stuff['title'], 
            "loc" : stuff['location'], 
            "url" : make_tiny(stuff['url'])} 
    _text = post["loc"] + "\n" + post["title"] +" " + post["url"]          
    _text = check_length(_text, post)
    return _text


def log(message):
    """Log message to logfile."""
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, logfile_username), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        print("\n" + t + " " + message) # print it tooo...
        f.write("\n" + t + " " + message)


def tweet(new_stuffs_set):
    """Tweet new free stuff."""
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)
    # Unpack set of sorted tuples back into dicts
    stuffs = map(dict, new_stuffs_set)
    if len(list(new_stuffs_set)) is not 0: # if there exists new items
        for stuff in stuffs:
            tweet = create_tweet(stuff)
            if str(stuff['image']) == NO_IMAGE:
                isImage = False 
            else:
                isImage = True
                urllib.request.urlretrieve(stuff['image'], FILE)
            try:
                if isImage:
                    log("\n\n Posting with Media \n " + tweet + "\n ----\n")
                    api.update_with_media(FILE, status=tweet)
                else: 
                    api.update_status(tweet)
                    log("\n\n Posting without media\n "
                         + tweet + "\n ----\n")
            except tweepy.error.TweepError as e:
                log(e.message)
    else:
        print("\n ----\n")


if __name__ == "__main__":
    """Tweet newly posted Free stuff objects.
    
    Using sets of the tupled-sorted-dict-stuffs to compare
    old scrapes and new. No need calling for precise, as 
    twitter doesn't need the coordinates. If the set has 15
    items, doesn't post, in order to stop flooding twitter
    on start up.
    """
    process_log = open(logfile_username,'a+')
    _location = 'newyork'
        stale_set = set() # the B set is what has already been 
    log("\n\nInitiating\n\n")
    while True:
        stuffs = [] # a list of dicts
        for stuff in Stuffify(_location, 15).get_freestuffs(): # convert stuff
            stuff_dict = {'title':stuff.thing,      # object into dict
                          'location':stuff.location, 
                          'url':stuff.url, 'image':stuff.image}
            stuffs.append(stuff_dict)
        fresh_set = set() # A set, Fresh out the oven
        for stuff in stuffs:
            tup = tuple(sorted(stuff.items()))
            fresh_set.add(tup)
        """Evaluate if there have been new posts"""
        ready_set = fresh_set - stale_set # Get the difference
        stale_set = fresh_set
        if len(list(ready_set)) is not 15:
            tweet(ready_set) 
        log("\n    New Stuffs : " + str(len(list(ready_set)))+
            "\n Todays Stuffs : "+ str(len(list(stale_set)))+
            "\n\n Sleep Now (-_-)Zzz... \n")
        sleep(3600) # 3600 Seconds = Hour
    
    
    
    
    
    
    
    
    
    
    
    
    
    
