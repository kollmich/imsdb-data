import requests 
import html5lib
from bs4 import BeautifulSoup 
import json
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import brown
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter


# read file
with open('data.txt', 'r') as myfile:
    data = json.load(myfile)

vulgarities = []

# GET LIST OF ALL OSCAR-WINNING MOVIES
URL_WIKTIONARY = "https://simple.wiktionary.org/wiki/Category:Vulgar"

wiki = requests.get(URL_WIKTIONARY) 

soup = BeautifulSoup(wiki.content, 'html5lib') 

vulgarities_div = soup.find('div', attrs = {'class':'mw-category'}).findAll('li')
for i in vulgarities_div:
    word = i.find('a').text
    vulgarities.append(word)

print(vulgarities)

for index in range(len(data)):
    #for key in data[index]:
    tokenized_word = word_tokenize(data[index]['subtitles'])
    wordcounts = Counter(tokenized_word)
    vulgar_count = 0
    for j in vulgarities:
        vulgar_count += wordcounts[j]

    print(data[index]['title']+' - vulgarities total: ' + str(vulgar_count))



