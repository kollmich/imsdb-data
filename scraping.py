import requests 
import html5lib
from bs4 import BeautifulSoup 
import re
import json


timeout = 100

# GET LIST OF ALL OSCAR-WINNING MOVIES
URL_ROTTEN_1 = "https://editorial.rottentomatoes.com/guide/oscars-best-and-worst-best-pictures/"
URL_ROTTEN_2 = "https://editorial.rottentomatoes.com/guide/oscars-best-and-worst-best-pictures/2/"

rot_1 = requests.get(URL_ROTTEN_1) 
rot_2 = requests.get(URL_ROTTEN_2) 

soup_01 = BeautifulSoup(rot_1.content, 'html5lib') 
soup_02 = BeautifulSoup(rot_2.content, 'html5lib') 

movies = []

def get_movie_data(list):
    # INIT OBJECT
    class movie(object):
        def __init__(self):
            self.title = ""
            self.rating = ""
            self.year = ""
        def __repr__(self):
            return str(self)

    h2 = i.find('div', attrs = {'class':'article_movie_title'})
    title = h2.a.text.strip()
    year = h2.find('span', attrs = {'class':"subtle start-year"}).text.strip()
    rating = h2.find('span', attrs = {'class':"tMeterScore"}).text.strip()

    actors = []
    actors_div = i.find('div', attrs = {'class':'info cast'}).findAll('a')
    for j in actors_div:
        actor = j.text
        actors.append(actor)
    separator = ', '
    actors = separator.join(actors)

    director = i.find('div', attrs = {'class':"info director"}).a.text.strip()


    movie.title = title
    movie.year = year.replace('(','').replace(')','')
    movie.rating = rating.replace('%','')
    movie.actors = actors
    movie.director = director

    i_subtitle = movie.title.replace(' ', '-')

    # SCRAPE AND LOAD SCRIPT TEXT
    URL_SCRIPT = "https://www.imsdb.com/scripts/" + i_subtitle + ".html"
    rs = requests.get(URL_SCRIPT) 
    if rs.status_code == 200:
        soup_2 = BeautifulSoup(rs.content, 'html5lib')
        if len(soup_2.find('td', attrs = {'class':'scrtext'}).get_text()) >= 1000:
            print(movie.title,": script found")
            script = soup_2.find('td', attrs = {'class':'scrtext'}).get_text().strip().replace("\n"," ")
            movie.script = script
            movies.append(movie)
        else:
            print(movie.title,": no script")
            script = "MISSING SCRIPT"
            movie.script = script
            movies.append(movie)
    else:
        print(movie.title,": url_failure")


divs_01 = soup_01.findAll('div', attrs = {'class':'col-sm-18 col-full-xs countdown-item-content'})
for i in divs_01:
    get_movie_data(movies)

divs_02 = soup_02.findAll('div', attrs = {'class':'col-sm-18 col-full-xs countdown-item-content'})
for i in divs_02:
    get_movie_data(movies)

for movie in movies:
    print(movie.title, movie.year, movie.rating, movie.actors, movie.director, movie.script)

# SAVE INTO SCV
import csv
with open('data.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['title', 'year', 'rating', 'actors', 'director', 'script'])
    for movie in movies:
        writer.writerow([movie.title, movie.year, movie.rating, movie.actors, movie.director, movie.script]) 
