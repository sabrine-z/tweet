'''
Created on 15 mai 2018

@author: acher
'''


import tkinter as tk
import Target   
import Analyse 
import DataCollection
import pandas as pd
from tkinter import StringVar



def Csv():
    MesCsv=tk.Tk()
    MesCsv.title("Les Csv Sont")
    MesCsv['bg']='white'
    S=Analyse.GetAll()
    for x in S: 
        Frame1 = tk.Frame(MesCsv,borderwidth=2,relief=tk.SUNKEN)
        Frame1.pack(side=tk.LEFT,padx=10,pady=10)
        tk.Label(Frame1,text=x).pack(padx=10,pady=10)

def mail():
    Contact=tk.Tk()
    Contact.title("Nous Contacter")
    Frame1 = tk.Frame(Contact,borderwidth=2,relief=tk.SUNKEN)
    Frame1.pack(side=tk.LEFT,padx=10,pady=10)
    tk.Label(Frame1,text="Contactez moi sur jmail.achref@gmail.com").pack(padx=10,pady=10)
    



def Collect(Key):
    DataCollection.Collection(str(Key), 100)


def KeyWord(journal):
    Keyword=tk.Tk()
    Keyword.title("Getting the Keyword")
    keys=Target.CollectTweets(journal)
    max=Target.max(keys[1])
    text=keys[0][max]
    parsed=text.split(' ')
    for i in range(len(parsed)):
        if (('/' not in parsed[i]) and (len(parsed[i])>2)):
            button=tk.Button(Keyword,text=parsed[i],bg="SkyBlue2",width=10,
                              command=lambda x=parsed[i]:Collect(x))
            button.pack()
    
    
    
    
         
def Data():
    journals=Target.ShowJournals()
    Data=tk.Tk()
    Data.title("Recuperation du journal")
    for x in journals:
        button=tk.Button(Data,text=x,bg="SkyBlue2",width=10,
                         command=lambda s=x:KeyWord(s))
        button.pack()
  
    
      
        

def addition():
    Add=tk.Tk()
    Add.title("Journal Addition")
    nom=StringVar(Add)
    recuperation_nom=nom.get()
    
    EntryJournal=tk.Entry(Add,textvariable=nom).grid()
    button1=tk.Button(Add,text="Add Journal",bg="SkyBlue2",width=10,
                  command=lambda:Target.AddJournal(recuperation_nom) )
    button1.grid(column=3)  
def Show(CSV):
    DF=pd.read_csv(CSV)
    Show=tk.Tk()
    Show.title(">>>Stat Plot<<<")
    button1=tk.Button(Show,text="histogramme",bg="SkyBlue2",width=10,
                         command=lambda :Analyse.Plothist(DF))
    button2=tk.Button(Show,text="BoxPlot",bg="SkyBlue2",width=10,
                         command=lambda :Analyse.PlotBox(DF))
    button3=tk.Button(Show,text="KdePlot",bg="SkyBlue2",width=10,
                         command=lambda :Analyse.PlotKdeplot(DF))
    button4=tk.Button(Show,text="DistPlot",bg="SkyBlue2",width=10,
                         command=lambda :Analyse.PlotDistplot(DF))
    button5=tk.Button(Show,text="ViolinPlot",bg="SkyBlue2",width=10,
                         command=lambda :Analyse.PlotViolinplot(DF))
    button1.pack()
    button2.pack()
    button3.pack()
    button4.pack()
    button5.pack()
def Plots():
    plot=tk.Tk()
    plot.title(">>>Data Choice<<<")
    DFList=Analyse.GetAll()
    for x in DFList:
        button=tk.Button(plot,text=x,bg="SkyBlue2",width=10,
                         command=lambda s=x:Show(s))
        button.pack()


    
root=tk.Tk()
root.title("Twitter Up To Date")
root.geometry("350x200")
menubar=tk.Menu(root)
menu1 = tk.Menu(menubar, tearoff=0)
menu1.add_command(label="Afficher mes csv", command=Csv)
menu1.add_separator()
menu1.add_command(label="Plots",command=Plots)
menu1.add_separator()
menu1.add_command(label="Quitter", command=root.quit)
menubar.add_cascade(label="Fichier", menu=menu1)

menu2 = tk.Menu(menubar, tearoff=0)
menu2.add_command(label="Add source", command=lambda:addition())
menubar.add_cascade(label="Editer", menu=menu2)

menu3 = tk.Menu(menubar, tearoff=0)
menu3.add_command(label="A propos", command=mail)
menubar.add_cascade(label="Aide", menu=menu3)
root.config(menu=menubar)
button1=tk.Button(root,text="Collect Data",bg="SkyBlue2",width=50,
                  command=Data)
button1.grid( column=7)


root.mainloop()
