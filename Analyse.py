'''
Created on 26 avr. 2018

@author: acher
'''
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import  sys
import codecs
import os
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)


#Configuration of sns
sns.set_palette("deep",desat=.6)
sns.set_context(rc={'figure.gigraize':(8,4)})

#Getting all the data collected
def GetAll():
    df_list = []
    path = os.path.dirname(__file__)
    dirs = os.listdir(path)
    for file in dirs:
        if '.csv' in file:
            df_list.append(file)
    return df_list




#Showing plots of a dataframe
def Plothist(DF):
    
    plt.hist((DF[DF.polarity!=0].polarity).dropna(),bins=8,color=sns.desaturate('indianred',1))   
    plt.show()


def PlotBox(DF):
    sns.boxplot((DF[DF.polarity!=0].polarity).dropna().dropna())
    plt.show()
    
def PlotKdeplot(DF):    
    sns.kdeplot((DF[DF.polarity!=0].polarity).dropna(),shade=True)
    plt.show()
def PlotDistplot(DF):
    sns.distplot((DF[DF.polarity!=0].polarity).dropna())
    plt.show()

def PlotViolinplot(DF):
    #in which point we have the highest probability
    sns.violinplot((DF[DF.polarity!=0].polarity).dropna())
    plt.show()



