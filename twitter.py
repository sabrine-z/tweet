
################################# imported module ###################################
import os#nous permet d'interagir avec le systeme d'exploitation
import subprocess#
from threading import Thread
from tkinter import *
from tkinter import ttk
import conf
import bs4
import requests
import tweepy
from matplotlib import pyplot as plt
from numpy import array
from textblob import TextBlob


class TwitterClient():

    def __init__(self):#Initialisation

        consumer_key = conf.consumer_key

        consumer_secret = conf.consumer_secret

        access_token = conf.access_token

        access_token_secret = conf.access_token_secret

        self.polarity = []# polarity=(count,query,positive,negative,neutral)
        self.count = 0
        self.query = 'lockdown'
        self.positive = 0
        self.negative = 0
        self.neutral = 0

        # tentative d'authentification
        try:

            # créer un objet OAuthHandler
            self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

            # définir le jeton d'accès et le secret
            self.auth.set_access_token(access_token, access_token_secret)

            # créer un objet API tweepy pour récupérer les tweets
            self.api = tweepy.API(self.auth)

        except:

            print("Error: Authentication Failed")

    def clean_tweet(self, tweet): #preparer les Data

        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):#créer un objet textBlob

        analysis = TextBlob(self.clean_tweet(tweet))
        self.polarity.append(analysis.sentiment.polarity)
        #calule de polarité
        # définir le sentiment
        if analysis.sentiment.polarity > 0:

            return 'positive'

        elif analysis.sentiment.polarity == 0:

            return 'neutral'

        else:

            return 'negative'
    #récuperer les tweets
    def get_tweets(self):

        tweets = []

        try:

            #appelez l'api twitter pour récupérer les tweets
            fetched_tweets = self.api.search(q=self.query, count=self.count)

            # # analyser les tweets un par un
            for tweet in fetched_tweets:

                # dictionnaire vide pour stocker les paramètres requis d'un tweet
                parsed_tweet = {}

                # sauvegarde du texte du tweet
                parsed_tweet['text'] = tweet.text

                # sauver le sentiment du tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # # ajout d'un tweet analysé à la liste des tweets
                if tweet.retweet_count > 0:

                    # si le tweet a des retweets, assurez-vous qu'il ne soit ajouté qu'une seule fois
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)

                else:

                    tweets.append(parsed_tweet)

                    # retourner des tweets analysés
            return tweets

        except tweepy.TweepError as e:

            # erreur d'impression (le cas échéant)
            print("Error : " + str(e))

            f = open("logbook.txt", "a")

            f.write("\n" + str(e))

            f.close()

    def plotPieChart(self):#plot PieCHart

        labels = ['Positive {:.2f} %'.format(self.positive), 'Neutral {:.2f} %'.format(self.neutral),
                  'Negative {:.2f} %'.format(self.negative)]

        sizes = [self.positive, self.neutral, self.negative]

        colors = ['green', 'orange', 'red']

        plt.figure(1)

        patches, texts = plt.pie(sizes, colors=colors, startangle=90)

        plt.legend(patches, labels, loc="best")

        plt.title('pie - chart')

        plt.axis('equal')

        plt.show()

    def scatter_plot(self):#plot scatter plot

        fig = plt.figure(2)

        axis = fig.add_subplot(1, 1, 1)

        x = array(range(0, len(self.polarity)))

        y = array(self.polarity)

        axis.plot(x, y)

        plt.xlabel('tweet number')

        plt.ylabel('polarity')

        plt.show()

    def plothistogram(self):#plot Histogram

        plt.figure(3)

        plt.hist(self.polarity, bins=7, color='green', histtype='barstacked')

        plt.ylabel('number of tweets')

        plt.xlabel('polarity of tweets')

        plt.show()


def cleartag():#
    tag.delete(0, END)

#nombre de tweets
def Select_number_of_tweets(event=None):
    return number_of_tweets.get()


def Select_trending_topic(event=None):
    api.query = str(topic.get())

    tag.delete(0, END)

    tag.insert(0, api.query)


def main():
    user_input = str(tag.get())

    if (len(user_input) > 1): #si user_input >1 on commence le travail
        api.query = str(user_input)

    api.count = Select_number_of_tweets()

    api.polarity = []

    print(api.query, api.count, len(api.polarity))

    search_button.config(text="fetching..")

    search_button.config(state=DISABLED)

    clear_button.config(text="Wait")

    clear_button.config(state=DISABLED)

    # fonction d'appel pour obtenir des tweets
    tweets = api.get_tweets()

    # choisir des tweets positifs à partir de tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment']=='positive']

    # pourcentage de tweets positifs
    api.positive = 100 * len(ptweets) / len(tweets)
    #afficher le résultat
    print("Positive tweets percentage: {:.2f} %".format(api.positive))

    # choisir des tweets négatifs à partir de tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    # percentage of negative tweets
    api.negative = 100 * len(ntweets) / len(tweets)
    #afficher le résultat
    print("Negative tweets percentage: {:.2f} %".format(api.negative))

    # pourcentage de tweets neutres
    api.neutral = 100 - api.positive - api.negative
    #afficher le résultat
    print("Neutral tweets percentage: {:.2f} %".format(api.neutral))

    # Les 10 premiers tweets positifs
    print("\n\nPositive tweets:")

    for tweet in ptweets[:10]:
        print(tweet['text'])

    # Les 10 premiers tweets négatifs
    print("\n\nNegative tweets:")

    for tweet in ntweets[:10]:
        print(tweet['text'])
    #construire les boutons
    search_button.config(text="Search")#Boutton Search

    search_button.config(state=NORMAL)

    clear_button.config(text="Clear")# Boutton Clean

    clear_button.config(state=NORMAL)


def main_thread():
    thread = Thread(target=main)#des portions de notre code qui sera exécutées en méme temps

    thread.start()

#accéder au site
def get_html(url):
    reponse = requests.get(url)#envoi d'une requét get et enregistrement de la reponse en tant qu'objet de réponse

    return reponse


def get_detail(): #les meileurs hashtags en france
    try:

        url = "https://trends24.in/france/"

        reponse = get_html(url)

        bs = bs4.BeautifulSoup(reponse.text, 'html.parser')

        tag = bs.find("div", class_="trend-card").find_all("a")

        trending = []

        for i in tag:
            trending.append(i.get_text())

        return trending

    except Exception as e:

        print(e)

        f = open("logbook.txt", "a")

        f.write("\n" + str(e))

        f.close()


def set_bg_to_grey():#changer la couleurs de l'interface en gris
    root.configure(background="grey")

    topframe.configure(background="grey")

    set_bg_frame.configure(background="grey")

    frame.configure(background="grey")

    middleframe.configure(background="grey")

    bottomFrame.configure(background="grey")


def set_bg_to_red():#changer la couleurs de l'interface en rouge
    root.configure(background="red")

    topframe.configure(background="red")

    set_bg_frame.configure(background="red")

    frame.configure(background="red")

    middleframe.configure(background="red")

    bottomFrame.configure(background="red")


def set_bg_to_pink():#changer la couleurs de l'interface en rose
    root.configure(background="pink")

    topframe.configure(background="pink")

    set_bg_frame.configure(background="pink")

    frame.configure(background="pink")

    middleframe.configure(background="pink")

    bottomFrame.configure(background="pink")


def set_bg_to_brown():#changer la couleurs de l'interface en marron
    root.configure(background="brown")

    topframe.configure(background="brown")

    set_bg_frame.configure(background="brown")

    frame.configure(background="brown")

    middleframe.configure(background="brown")

    bottomFrame.configure(background="brown")


def set_bg_to_green():#changer la couleurs de l'interface en vert
    root.configure(background="green")

    topframe.configure(background="green")

    set_bg_frame.configure(background="green")

    frame.configure(background="green")

    middleframe.configure(background="green")

    bottomFrame.configure(background="green")


def set_bg_to_blue():#changer la couleurs de l'interface en bleu
    root.configure(background="lightblue")

    topframe.configure(background="lightblue")

    set_bg_frame.configure(background="lightblue")

    frame.configure(background="lightblue")

    middleframe.configure(background="lightblue")

    bottomFrame.configure(background="lightblue")


def open_twitter():#accéder a un page web twitter
    twitter_url = "https://twitter.com/"

    if sys.platform.startswith('linux'):

        subprocess.Popen(['xdg-open', twitter_url],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    elif sys.platform.startswith('win32'):

        os.startfile(twitter_url)

    elif sys.platform.startswith('cygwin'):

        os.startfile(twitter_url)

    elif sys.platform.startswith('darwin'):

        subprocess.Popen(['open', twitter_url],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:

        subprocess.Popen(['xdg-open', twitter_url],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)




if __name__ == "__main__":
    # appel de la fonction principale
    api = TwitterClient()#crée une instance de la Class TwitterClient

    root = Tk()#crée un interface graphique

    root.title("Twitter Sentiment Analysis Desktop Application")#titre de l'interface

    root.geometry("800x600")#dimention de l'interface

    root.resizable(width=False, height=False)

    root.configure(background="lightblue")#couleur de l'interface graphique
    # création d'un widget Label (text'Twitter Sentiment Analysis')
    label1 = Label(root, text="Twitter Sentiment Analysis", fg="blue", bg="skyblue", font=("", 15, "bold"))
    label1.pack(side=TOP, pady=20)#Positionnement du widget avec la methode pack()

    topframe = Frame(root, background="lightblue")

    topframe.pack()#Positionnement du widget avec la methode pack()

    set_bg_frame = Frame(topframe, background="lightblue", height=150, width=150)

    set_bg_frame.pack(side=LEFT)#Positionnement du widget avec la methode pack()


    darkcolor = Frame(set_bg_frame)

    darkcolor.pack()#Positionnement du widget avec la methode pack()

    lightcolor = Frame(set_bg_frame)

    lightcolor.pack()#Positionnement du widget avec la methode pack()

    red_image = PhotoImage(file="red.png")

    brown_image = PhotoImage(file="brown.png")

    pink_image = PhotoImage(file="pink.png")

    grey_image = PhotoImage(file="grey.png")

    green_image = PhotoImage(file="green.png")

    blue_image = PhotoImage(file="blue.png")

    red_image = red_image.subsample(4, 4)

    brown_image = brown_image.subsample(4, 4)

    pink_image = pink_image.subsample(4, 4)

    grey_image = grey_image.subsample(4, 4)

    green_image = green_image.subsample(4, 4)

    blue_image = blue_image.subsample(4, 4)

    red_button = Button(darkcolor, image=red_image, command=set_bg_to_red)

    red_button.pack(side=LEFT)#Positionnement du widget avec la methode pack()

    brown_button = Button(darkcolor, image=brown_image, command=set_bg_to_brown)

    brown_button.pack(side=LEFT)#Positionnement du widget avec la methode pack()

    green_button = Button(darkcolor, image=green_image, command=set_bg_to_green)

    green_button.pack(side=LEFT)

    pink_button = Button(lightcolor, image=pink_image, command=set_bg_to_pink)

    pink_button.pack(side=LEFT)

    grey_button = Button(lightcolor, image=grey_image, command=set_bg_to_grey)

    grey_button.pack(side=LEFT)

    blue_button = Button(lightcolor, image=blue_image, command=set_bg_to_blue)

    blue_button.pack(side=LEFT)
#creation du Bouton Twitter
    twitter_img = PhotoImage(file="twitter.png")

    twitter_img = twitter_img.subsample(1, 1)

    twitter_button = Button(topframe, image=twitter_img, command=open_twitter)

    twitter_button.pack(side=LEFT, padx=(100, 60))

    frame = Frame(topframe, background="lightblue")

    frame.pack(side=LEFT)

    label6 = Label(frame, text="Trending #tag", fg="red", bg="blue", font=("", 12, "bold"))

    label6.pack(side=TOP, pady=10)

    topic = StringVar()

    trending_topics = ttk.Combobox(frame, textvariable=topic, width=20, height=10)

    #case de meilleur hashtage
    trending_topics['values'] = get_detail()

    trending_topics.pack()

    trending_topics.current(0)

    trending_topics.bind("<<ComboboxSelected>>", Select_trending_topic)
    # saisir votre hashtage que vous voulez chercher
    label3 = Label(root, text="Enter Twitter #tag to search", fg="red", bg="yellow", font=("", 12, "bold"))

    label3.pack(side=TOP, pady=10)

    tag = Entry(root, justify=CENTER, font=("verdana", "15", "bold"))

    tag.pack(side=TOP)

    middleframe = Frame(root, background="lightblue")

    middleframe.pack()

    search_button = Button(middleframe, text="Search", fg="white", bg="black", height=1, width=10,#boutton search
                           font=("verdana", 10, "bold"), command=main_thread)

    search_button.pack(side=LEFT, padx=5, pady=5)

    clear_button = Button(middleframe, text="Clear", fg="white", bg="black", height=1, width=10,#boutton clean
                          font=("verdana", 10, "bold"), command=cleartag)

    clear_button.pack(side=LEFT, padx=5, pady=5)

    label4 = Label(root, text="Select number of tweets to fetch from twitter", fg="red", bg="yellow",   #choix de nombre de tweet à chercher
                   font=("", 12, "bold"))

    label4.pack(side=TOP, pady=10)

    Values = (50, 75, 100, 150, 200, 250, 500, 750, 1000)#list des choix du nombre de tweet

    number_of_tweets = IntVar()

    choices = ttk.Combobox(root, textvariable=number_of_tweets, height=10)

    choices['values'] = Values

    choices.pack()

    choices.current(2)

    choices.bind("<<ComboboxSelected>>", Select_number_of_tweets)

    label5 = Label(root, text="Select appropriate diagram to dislpay ", fg="red", bg="yellow", font=("", 12, "bold"))

    label5.pack(side=TOP, pady=10)

    bottomFrame = Frame(root, background="lightblue", width=700, height=150)

    bottomFrame.pack(side=TOP, pady=20)

    piechart_image = PhotoImage(file="piechart.png")#boutton image pour afficher le graph Pie Chart

    scatterplot_image = PhotoImage(file="scatter.png")#boutton image pour afficher le graph scatter

    histogram_image = PhotoImage(file="histogram.png")#boutton image pour afficher le graph histogram

    piechart_image = piechart_image.subsample(2, 2)

    scatterplot_image = scatterplot_image.subsample(2, 2)

    histogram_image = histogram_image.subsample(2, 2)

    piechart_button = Button(bottomFrame, image=piechart_image, command=api.plotPieChart)

    piechart_button.pack(side=LEFT, padx=20)

    scatterplot_button = Button(bottomFrame, image=scatterplot_image, command=api.scatter_plot)

    scatterplot_button.pack(side=LEFT, padx=20)

    histogram_button = Button(bottomFrame, image=histogram_image, command=api.plothistogram)

    histogram_button.pack(side=LEFT, padx=20)


    root.mainloop()# lancement deu gestionnaire d'événements