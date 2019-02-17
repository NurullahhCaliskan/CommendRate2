import csv
import pandas as pd
import numpy as np

from string import punctuation,digits
from ngram import NGram

from joblib import load
from tkinter import *


def sonucbul():
    kelimeler = list()

    v = NGram(ngramdatawords)
    sonucthreshold = list()
    sonuckelime = list()

    kelimedizisi = np.zeros((1, len(ngramdatawords)), dtype='int8')
    yorum = e1.get() ###############
    cevirici = str.maketrans('', '', punctuation)
    yorum = yorum.translate(cevirici)
    cevirici = str.maketrans('', '', digits)
    yorum = yorum.translate(cevirici)
    yorum = yorum.lower()
    kelimeler.clear()
    kelimeler = yorum.split()
    for j in range(0, len(kelimeler), 1):
        sonucthreshold.clear()
        sonuckelime.clear()
        for ngrami in v.search(kelimeler[j], threshold=0.4):
            sonuckelime.append(str(ngrami[0]))
            sonucthreshold.append(int(ngrami[1]))
        if (len(sonuckelime) != 0):
            kelimedizisi[0][ngramdatawords.index(sonuckelime[sonucthreshold.index(max(sonucthreshold))])] += 1
    tmpdf = pd.DataFrame(kelimedizisi)
    sonuc = ngrammodel.predict(tmpdf)
    cevirici = str.maketrans('', '', punctuation)
    cevap=str(sonuc).translate(cevirici)
    print("Yorum= " + yorum + " Yorum Sonucu= " + str(sonuc))

    e1.delete(0, END)
    Label(master, text="Puan(1-5) ="+str(cevap)).grid(row=2)


def wordcleaner(word):
    return str(word).replace("[", "").replace("]", "").replace(",", "").replace("'", "")

with open(r'CSV\Puan.csv', newline='',encoding="utf-8") as csvfile:
    puanlist = list(csv.reader(csvfile))



with open(r'CSV\ngramwords.csv', newline='',encoding="utf-8") as csvfile:         ################################
    ngramdatawords = list(csv.reader(csvfile))

ngrammodel=load(r'Models\NGramDataMultinomialNB.joblib')


for i in range(len(ngramdatawords)):
    ngramdatawords[i]=wordcleaner(ngramdatawords[i])
for i in range(len(puanlist)):
    puanlist[i] = wordcleaner(str(puanlist[i]))

master = Tk()
Label(master, text="Yorumunuzu giriniz").grid(row=0)


e1 = Entry(master)



e1.grid(row=0, column=1)


Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=W, pady=4)
Button(master, text='Show', command=sonucbul).grid(row=3, column=1, sticky=W, pady=4)

mainloop( )









