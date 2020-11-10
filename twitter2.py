from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Cursor
from tweepy import API
import conf
import matplotlib.pyplot as plt
import time
import json
import tkinter as tk
import sys
import os
#initialisations de nos variables
TWITTER_COLOR = '#00acee'
buttonPressed = False
numTweets = 0#initialisation du nombre tweets
elapsedTime = 0
finalTime = 0#initialisation
seconds = 1
yTweets = []
xSeconds = []
graphfont = {'family': 'Lucida Console',
             'color': TWITTER_COLOR,
             'weight': 'normal',
             'size': 16,
             }#definir le style d'interface

#obtenir nos clés et nos jetons
consumer_key = conf.consumer_key
consumer_secret = conf.consumer_secret
access_token = conf.access_token
access_token_secret = conf.access_token_secret

class Client():#creation de client de l'API tweepy
    def __init__(self, user=None):
        self.auth = Authenticator().Authenticate()
        self.client = API(self.auth)
        self.user = user

    def getClient(self):
        return self.client


class Authenticator():
    def Authenticate(self):
        auth = OAuthHandler(consumer_key, consumer_secret)            # créer un objet OAuthHandler
        auth.set_access_token(access_token, access_token_secret)            # définir le jeton d'accès et le secret
        return auth


class TweetViewer():
    """
    Proccess Live Tweets
    """

    def __init__(self):
        self.authenticator = Authenticator()#crée une instance de la Class Authenticator

    def FetchTweets(self, filename, filter):
        listener = Listener(filename)#crée une instance de la Class Listener
        auth = self.authenticator.Authenticate()
        stream = Stream(auth, listener)
        global topics
        stream.filter(track=topics, is_async=True, languages=['en'])#la langue des tweets
        global buttonPressed
        if (buttonPressed == True):
            stream.filter.track\
                = None
            stream.disconnect()
            stream = None
            # topics[0] = ''


class Listener(StreamListener):
    """
    Prints tweet contents
    """

    def __init__(self, filename):
        self.filename = filename

    def on_data(self, data):
        try:
            global buttonPressed
            if buttonPressed == False and len(topics) > 0:#on grade les memes valeurs des variable si on ne clique pas sur 'buttonPressed'
                global elapsedTime
                global finalTime
                global seconds
                global numTweets
                yTweets.append(numTweets)
                xSeconds.append((time.time() - elapsedTime))
                # seconds += seconds
                d = json.loads(data)
                # print("Topic is: ", topics, "buttonPressed is: ", buttonPressed)
                formatted = convert65536('@' + d['user']['screen_name'] + ": " + d['text'])
                text.insert(tk.END, formatted)
                text.insert(tk.END, "\n\n")
                text.see(tk.END)
                numTweets = numTweets + 1
                numTweetsLabel.configure(text="Tweets: {0}".format(numTweets), bg='black', fg=TWITTER_COLOR, font=40)
                return True
            else:
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        # print(data)
        return True

    def on_error(self, status):#traitement d'erreur '420'
        if status == 420:
            return False
        print(status)
        return True


# traitement des emojis et autres personnages non unicode qui peuvent apparaître dans les tweets
def convert65536(s):  #######################################
    l = list(s);  #
    i = 0;  #
    while i < len(l):  #
        o = ord(l[i]);  # https://stackoverflow.com/a/28076205
        if o > 65535:  #
            l[i] = "{" + str(o) + "u}";  #
        i += 1;  #
    return "".join(l);  ########################################


firstPress = True


def onButtonPress():
    global buttonPressed#mettre a jour les variable
    global Viewer
    global topics
    global file
    global elapsedTime
    global firstPress
    if firstPress == True:
        elapsedTime = time.time()#counter le temps passe pour touver et affiche les tweets
        firstPress = False
    buttonPressed = True
    topics.insert(0, TextBox.get())#
    topicsLabel.configure(text="Current Topics:\n {0}".format(printTopicsListVertical(topics)), bg='black',
                          fg=TWITTER_COLOR, font=40, anchor='n', bd=10)#sauvegarder les mot clé utilisées

    if (len(topics) > 0):#afficher les tweets
        buttonPressed = False
        Viewer.FetchTweets(file, topics)#REcupérer le fichier json et afficher son contenue



def onResetButtonPress():#fonction pour remise a l'etat intial
    global finalTime
    global elapsedTime
    finalTime = time.time() - elapsedTime
    print(finalTime)

    global buttonPressed
    buttonPressed = True
    global numTweets
    numTweetsLabel.configure(text="Tweets: {0}".format(numTweets))
    graph()
    numTweets = 0


def onExitButtonPress():#boutton quitter
    root.destroy()
    sys.exit(0)


def printTopicsList(topics):#zone de recherche
    if len(topics) == 1:
        return topics[0]

    s = ", ".join(topics)
    return s


def printTopicsListVertical(topics):#list de mot cle sauvgardé
    if len(topics) == 1:
        return topics[0]

    s = "\n".join(topics)
    return s


def graph():#affiche le graph
    global elapsedTime
    global finalTime
    plt.xlabel('time (sec)', fontdict=graphfont)
    plt.ylabel('Tweets', fontdict=graphfont)
    plt.title('Number of Tweets about {0} over {1} seconds'.format(printTopicsList(topics), int(finalTime + 1.0)),
              fontdict=graphfont)
    plt.plot(xSeconds, yTweets, TWITTER_COLOR)
    plt.show()


topics = []
file = "tweets.json"#creation d'un fichier json
Viewer = TweetViewer()

myClient = Client()
api = myClient.getClient()
tweets = api.user_timeline(screen_name="realDonaldTrump", count=10)

mandotweets = []
HEIGHT = 720
WIDTH = 1280
#  appel de la fonction principale
root = tk.Tk()#créer un interface graphique
root.title("LiveTweets")#titre de l'interface
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack() #Positionnement du widget avec la methode pack()

background = tk.PhotoImage(file='background.png')#inserer image au fond
bgLabel = tk.Label(root, image=background)
bgLabel.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg=TWITTER_COLOR, bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')
#affichage du texbox
TextBox = tk.Entry(frame, bg='white', font=200)
TextBox.bind("<Return>", (lambda event: onButtonPress()))
TextBox.place(relwidth=0.65, relheight=1)

button = tk.Button(frame, text="Add Topic to Live Feed", bg='#00acee', fg='white', font=40, command=onButtonPress)
button.place(relx=0.6, relheight=1, relwidth=0.29)

stopButton = tk.Button(frame, text="Graph Tweets/\nStop Feed", bg='#000080', fg='white', font=40,
                       command=onResetButtonPress, borderwidth=3, relief="raised")
stopButton.place(relx=0.88, relheight=1, relwidth=0.12)

exitButton = tk.Button(root, text="Exit", bg=TWITTER_COLOR, fg='white', font=80, command=onExitButtonPress,
                       borderwidth=3, relief="raised")
exitButton.place(relheight=0.1, relwidth=0.1, relx=0.45, rely=0.85)

numTweetsLabel = tk.Label(root, text="Tweets: {0}".format(numTweets), borderwidth=3, relief="ridge")
numTweetsLabel.configure(text="Tweets: {0}".format(numTweets), bg='black', fg=TWITTER_COLOR, font=40)
numTweetsLabel.place(relheight=0.1, relwidth=0.15, relx=0.6, rely=0.85)

topicsLabel = tk.Label(root, text="Current Topics:\n {0}".format(printTopicsList(topics)), borderwidth=3,
                       relief="ridge")
topicsLabel.configure(text="Current Topics:\n {0}".format(printTopicsList(topics)), bg='black', fg=TWITTER_COLOR,
                      font=40, anchor='n', bd=10)
topicsLabel.place(relheight=0.6, relwidth=0.12, relx=0.004, rely=0.25)

frame2 = tk.Frame(root, bg=TWITTER_COLOR, bd=10)
frame2.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

text = tk.Text(frame2)
text.config(state='normal')
text.config(font=("Lucida"))
text.place(relwidth=1, relheight=1)

# text.insert(tk.END, convert65536(str(TheTweets)))
root.mainloop()
# END OF GUI LOOP