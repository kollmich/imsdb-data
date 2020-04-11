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
import csv
import json
import pandas as pd

# read file
with open('output/data.txt', 'r') as myfile:
    data = json.load(myfile)
# GET LIST OF VULGAR WORDS FROM WIKIPEDIA
# vulgarities = []
# URL_WIKTIONARY = "https://simple.wiktionary.org/wiki/Category:Vulgar"

# wiki = requests.get(URL_WIKTIONARY) 

# soup = BeautifulSoup(wiki.content, 'html5lib') 

# vulgarities_div = soup.find('div', attrs = {'class':'mw-category'}).findAll('li')
# for i in vulgarities_div:
#     word = i.find('a').text
#     vulgarities.append(word)

# EXPLICITLY DEFINED LIST OF VULGARITIES
vulgarities = ["asshole", "bastard", "bitch", "cunt", "dick", "dickhead", "faggot", "fuck", "fucked", "fucker", "fucking", "nigga", "nigger", "shit", "shittier", "shittiest", "shitty", "slut"]

# COUNT VULGAR WORDS IN SUBTITLES AND SAVE AS VULGAR_COUNT IN DATASET
for index in range(len(data)):
    #for key in data[index]:
    tokenized_subs = word_tokenize(data[index]['subtitles'])
    wordcounts = Counter(tokenized_subs)
    def remove_stopwords(subs):
        return [w for w in subs if w not in stop_words]
    stop_words = list(set(stopwords.words('english')))

    tokenized_subs = remove_stopwords(tokenized_subs)
        
    # print(wordcounts)
    vulgar_count = 0
    for j in vulgarities:
        vulgar_count += wordcounts[j]
        data[index][j] = wordcounts[j]

    data[index]['vulgarities_count'] = vulgar_count
    data[index]['tokenized_subs'] = tokenized_subs

    analysis = TextBlob(data[index]['subtitles'])

    data[index]['sentiment'] = analysis.sentiment[0]
    data[index]['subjectivity'] = analysis.sentiment[1]

    data[index]['fuck'] = data[index]['fuck'] + data[index]['fucker'] + data[index]['fucking'] + data[index]['fucked']
    data[index]['nigger'] = data[index]['nigger'] + data[index]['nigga']
    data[index]['shit'] = data[index]['shit'] + data[index]['shittier'] + data[index]['shittiest'] + data[index]['shitty']
    data[index]['dick'] = data[index]['dick'] + data[index]['dickhead']

datax=[]
for index in range(len(data)):
    title = {"title": data[index]['title'], 
            "year": data[index]['year'], 
            "rating": data[index]['rating'],
            #"actors": data[index]['actors'], 
            # "director": data[index]['director'],
            "vulgarities": data[index]['vulgarities_count'], 
            "sentiment": data[index]['sentiment'],
            "subjectivity": data[index]['subjectivity'] }
    for j in vulgarities:
        title[j] =  data[index][j] 
    datax.append(title)

movies_json=json.dumps(datax)

df = pd.read_json(movies_json)
df = df.drop(['fucker', 'fucking', 'fucked', 'nigga', 'shittier', 'shittiest', 'shitty', 'dickhead'], axis=1)
df['year'] = pd.to_datetime(df['year'].astype(str) + "01" + "01", format='%Y%m%d')
#REMOVE DUPLICATES
df.drop_duplicates(keep='first', inplace=True) 
#SORT BY YEAR
df.sort_values(by='year', ascending=True, inplace=True)
print(df)
df.to_csv('output/data_sentiment.csv', index = False)

aggregates = df.groupby('year').agg(
        movies_count = pd.NamedAgg(column='title',aggfunc='count'),
        vulgarities = pd.NamedAgg(column='vulgarities',aggfunc=sum),
        asshole = pd.NamedAgg(column='asshole',aggfunc=sum),
        bastard = pd.NamedAgg(column='bastard',aggfunc=sum),
        bitch = pd.NamedAgg(column='bitch',aggfunc=sum),
        cunt = pd.NamedAgg(column='cunt',aggfunc=sum),
        dick = pd.NamedAgg(column='dick',aggfunc=sum),
        faggot = pd.NamedAgg(column='faggot',aggfunc=sum),
        fuck = pd.NamedAgg(column='fuck',aggfunc=sum),
        nigger = pd.NamedAgg(column='nigger',aggfunc=sum),
        shit = pd.NamedAgg(column='shit',aggfunc=sum),
        slut = pd.NamedAgg(column='slut',aggfunc=sum),
)

aggregates['vulgarities_rel'] = aggregates['vulgarities'] / aggregates['movies_count']
aggregates['asshole_rel'] = aggregates['asshole'] / aggregates['movies_count']
aggregates['bastard_rel'] = aggregates['bastard'] / aggregates['movies_count']
aggregates['bitch_rel'] = aggregates['bitch'] / aggregates['movies_count']
aggregates['cunt_rel'] = aggregates['cunt'] / aggregates['movies_count']
aggregates['dick_rel'] = aggregates['dick'] / aggregates['movies_count']
aggregates['faggot_rel'] = aggregates['faggot'] / aggregates['movies_count']
aggregates['fuck_rel'] = aggregates['fuck'] / aggregates['movies_count']
aggregates['nigger_rel'] = aggregates['nigger'] / aggregates['movies_count']
aggregates['shit_rel'] = aggregates['shit'] / aggregates['movies_count']
aggregates['slut_rel'] = aggregates['slut'] / aggregates['movies_count']

aggregates.round(3).to_csv('output/data_aggs.csv', index = True)



