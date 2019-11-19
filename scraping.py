import requests 
import html5lib
from bs4 import BeautifulSoup 
import re

movies_list = ['Collateral','Alien']

movies = []

class movie():
    def __init__(self):
        self.title = ""
        self.rating = ""
        self.authors = ""
        self.genres = ""
        self.date = ""

    def __repr__(self):
        return str(self)

for i in movies_list:

    URL_INFO = "https://www.imsdb.com/Movie%20Scripts/" + i + "%20Script.html"
    URL_SCRIPT = "https://www.imsdb.com/scripts/" + i + ".html"

    r = requests.get(URL_INFO) 

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
    separator = ', '
    authors = separator.join(authors)

    genres_start = script_details.tbody.contents[2].find(string="Genres")
    genres = []
    next = genres_start.next_element
    while next.name != 'b':
        if next.name == 'a':
            genres.append(next.text)
        next = next.next_element

    genres = separator.join(genres)

    date = script_details.tbody.contents[2].find(string="Script Date").next_element.replace(' : ','')

    movie.title = title
    movie.rating = rating
    movie.authors = authors
    movie.genres = genres
    movie.date = date

    movies.append(movie)

    print(movie.title)

for movie in movies:
    print(movie.rating)

