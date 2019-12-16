import requests 
import html5lib
from bs4 import BeautifulSoup 
import json
import nltk
import re
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import brown
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
from nltk.corpus import stopwords
from textblob import TextBlob
import string

# read file
with open('data.txt', 'r') as myfile:
    data = json.load(myfile)

vulgarities = []

# GET A LIST OF ALL VULGAR WORDS
URL_WIKTIONARY = "https://simple.wiktionary.org/wiki/Category:Vulgar"

wiki = requests.get(URL_WIKTIONARY) 

soup = BeautifulSoup(wiki.content, 'html5lib') 

vulgarities_div = soup.find('div', attrs = {'class':'mw-category'}).findAll('li')
for i in vulgarities_div:
    word = i.find('a').text
    vulgarities.append(word)

# COUNT VULGAR WORDS IN SUBTITLES AND SAVE AS VULGAR_COUNT IN DATASET
for index in range(len(data)):
    #for key in data[index]:
    tokenized_subs = word_tokenize(data[index]['subtitles'])
    wordcounts = Counter(tokenized_subs)
    vulgar_count = 0
    for j in vulgarities:
        vulgar_count += wordcounts[j]

    data[index]['vulgarities_count'] = vulgar_count
    #print(data[index]['vulgarities_count'])

    stop_words = list(set(stopwords.words('english')))
    def remove_stopwords(subs):
        return [w for w in subs if w not in stop_words]

    tokenized_subs = remove_stopwords(tokenized_subs)
    data[index]['tokenized_subs'] = tokenized_subs

    analysis = TextBlob(data[index]['subtitles'])

    data[index]['sentiment'] = analysis.sentiment[0]
    data[index]['subjectivity'] = analysis.sentiment[1]

movies_json = [{"title": data[index]['title'], "year": data[index]['year'], 
                "rating": data[index]['rating'], "actors": data[index]['actors'], 
                "director": data[index]['director'],"vulgarities": data[index]['vulgarities_count'], 
                "sentiment": data[index]['sentiment'],"subjectivity": data[index]['subjectivity'] }
                for index in range(len(data))]

with open('data_sentiment.txt', 'w') as outfile:
    json.dump(movies_json, outfile)

    #CHART TOP 10 WORDS IN SUBS
    # print(nltk.FreqDist(tokenized_subs))
    # fig = plt.figure(figsize = (10,4))
    # plt.gcf().subplots_adjust(bottom=0.15) # to avoid x-ticks cut-off
    # fdist = nltk.FreqDist(tokenized_subs)
    # fdist.plot(10, cumulative=False)
    # plt.show()
    # fig.savefig('freqDist.png', bbox_inches = "tight")
