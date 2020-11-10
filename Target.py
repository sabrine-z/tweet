'''
Created on 10 mai 2018

@author: acher
'''

import tweepy
from time import sleep
#import sys
#import codecs
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



targets=['nytimes',"lemondefr",'lequipe']

def ShowJournals():
    return targets
def AddJournal(journal):
    targets.append(journal)
#Choosing Journal de nos propositions
'''
def ChoosingJournal():
    print("Avec quel journal voulez vous travailler")
    for i in range(len(targets)):
        print("Si "+targets[i]+" entrez "+str(i))
    x=-1
    while x not in range(len(targets)):
        try:
            x=int(input("Entrez votre choix de journal "))
        except ValueError:
            print("Retry")
            x=-1
    return targets[x]
'''        
        
        
#Collecting tweets Du Journal
def CollectTweets(target):     
    texte=list()
    likes=list()
    for status in tweepy.Cursor(api.user_timeline, id=target).items(20):
        texte.append(status.text)
        likes.append(status.retweet_count)
    return(texte,likes)

#Getting Keyword from a used Target
def Getkeyword(target):
    C=CollectTweets(target)
    i=max(C[1])
    tweet=C[0][i]
    parsed=tweet.split(' ')
    count_occur=[0 for i in range(len(parsed))]
    for j in range(len(parsed)):
        if(len(parsed[j])>4):
            for t in C[0]:
                if parsed[j] in t:
                    count_occur[j]+=1
    if max(count_occur)>3:
        
        return parsed[max(count_occur)]
    else:
        print("Vous voyez quel mot comme Keyword/n")
        for j in range(len(parsed)):
            print("pour "+parsed[j]+" entrez "+str(j))
        b=True
        x=len(parsed)-1
        while(b):
            try:
                x=int(input(" <<<Entrez votre String >>> "))
                if x in range(len(parsed)):
                    b=False
                else:
                    print("wrong number")
            except ValueError:
                print("Oup's >>>> wrong number ")
        
        return parsed[x]

def max(L):
    id_max=0
    for j in range(1,len(L)):
        if L[j]>L[id_max]:
            id_max=j
    return id_max        
