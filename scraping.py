import requests 
import html5lib
from bs4 import BeautifulSoup 
import re

URL = "https://www.imsdb.com/Movie%20Scripts/Jackie%20Brown%20Script.html"
r = requests.get(URL) 

soup = BeautifulSoup(r.content, 'html5lib') 

script_details = soup.find('table', attrs = {'class':'script-details'})



title = script_details.h1.text.replace(' Script', '')
rating = script_details.tbody.contents[2].find(string="Average user rating").next_element.next_element.next_element.next_element.replace(' (','')[0:3]
author = script_details.tbody.contents[2].find(string="Writers").next_element.next_element.next_element.text
date = script_details.tbody.contents[2].find(string="Script Date").next_element.replace(' : ','')
genres = script_details.tbody.contents[2].find(string="Genres")

print(title)
print(rating)
print(author)
print(date)
