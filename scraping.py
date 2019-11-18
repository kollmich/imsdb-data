import requests 
import html5lib
from bs4 import BeautifulSoup 
import re

URL = "https://www.imsdb.com/Movie%20Scripts/Collateral%20Script.html"
r = requests.get(URL) 

soup = BeautifulSoup(r.content, 'html5lib') 

script_details = soup.find('table', attrs = {'class':'script-details'})

title = script_details.h1.text.replace(' Script', '')
rating = script_details.tbody.contents[2].find(string="Average user rating").next_element.next_element.next_element.next_element.replace(' (','')[0:3]
author_start = script_details.tbody.contents[2].find(string="Writers")
authors = []
next = author_start.next_element
while next.name != 'b':
    if next.name == 'a':
        authors.append(next.text)
    next = next.next_element

genres_start = script_details.tbody.contents[2].find(string="Genres")
genres = []
next = genres_start.next_element
while next.name != 'b':
    if next.name == 'a':
        genres.append(next.text)
    next = next.next_element

date = script_details.tbody.contents[2].find(string="Script Date").next_element.replace(' : ','')

print(title)
print(rating)
print(authors)
print(genres)
print(date)
