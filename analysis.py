import requests 
import html5lib
from bs4 import BeautifulSoup 
import json
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import brown
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
from nltk.corpus import stopwords
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

    stop_words = list(set(stopwords.words('english')))
    def remove_stopwords(subs):
        return [w for w in subs if w not in stop_words]

    tokenized_subs = remove_stopwords(tokenized_subs)
    data[index]['tokenized_subs'] = tokenized_subs
    print(data[index]['tokenized_subs'])

