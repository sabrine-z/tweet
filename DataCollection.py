'''
Created on 23 avr. 2018

@author: acher
'''
import tweepy
from time import sleep
import csv
#import sys
#import codecs
from textblob import TextBlob
#sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)


# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="1q3MYHfKTMrIowx1tZ7PbtMHp"
consumer_secret="VZdg5inym57X5wIIa2GPdFo1BDLD2no3wDtCedzfTREEkepcaV"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token="986731591794872320-kdqqXvqJk04Z709rSBA7xt5pXUoFFei"
access_token_secret="C7p0pVzbpqm5sBLPWf8yrOKkqp1BFaxk51cD3dMJAG5Hv"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
print('>>>>>>>>>>>Connected')



fieldnames = ['key','text','polarity','subjectivity','location']

def Collection(OurKey,items):
    key=OurKey
    fieldnames = ['key','text','polarity','subjectivity','location','retweet']
    csvFile = open(key+'.csv', 'w',encoding='utf8')
    f=csv.DictWriter(csvFile,fieldnames=fieldnames)
    f.writeheader()
    for tweets in tweepy.Cursor(api.search,q=key).items(items):
        try:
           p=TextBlob(tweets.text)
           sentiments=p.sentiment
           f.writerow({'key':key,'text':tweets.text,'polarity':sentiments[0],
                       'subjectivity':sentiments[1],'retweet':tweets.retweet_count})
        except tweepy.TweepError as e:
            print(e.reason)
            sleep(10)    
        except StopIteration:
            break
    csvFile.close()
    print(key+"File Created")
    
    


 
    
