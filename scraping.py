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

movies = {}

def get_title_name(list):
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

    movie.title = title
    movie.year = year
    movie.rating = rating

    #default_data.update({'item3': 3})
    list[movie] = movie
    print(movie.title, movie.year, movie.rating)

divs_01 = soup_01.findAll('div', attrs = {'class':'col-sm-18 col-full-xs countdown-item-content'})
for i in divs_01:
    get_title_name(movies)

divs_02 = soup_02.findAll('div', attrs = {'class':'col-sm-18 col-full-xs countdown-item-content'})
for i in divs_02:
    get_title_name(movies)

for x in movies:
    print (x.title)
    # for y in movies[x]:
    #     print (y,':',movies[x][y])


# for i in movies_list:
#     i_info = i.replace(' ', '%20')
#     i_script = i.replace(' ', '-')
#     print(i)

#     # INIT OBJECT
#     class movie(object):
#         def __init__(self):
#             self.title = ""
#             self.rating = ""
#             self.authors = ""
#             self.genres = ""
#             self.date = ""

#         def __repr__(self):
#             return str(self)

#     # SCRAPE AND LOAD SCRIPT INFO
#     URL_INFO = "https://www.imsdb.com/Movie%20Scripts/" + i_info + "%20Script.html"
#     r = requests.get(URL_INFO)
#     if r.status_code == 200:
#          print("info_success")
#     else:
#         print("info_failure")

#     if (r.status_code == 200):
#         soup_1 = BeautifulSoup(r.content, 'html5lib')


#         if (soup_1.find('table', attrs = {'class':'script-details'})):

#             script_details = soup_1.find('table', attrs = {'class':'script-details'})

#             title = script_details.h1.text.replace(' Script', '')
#             rating = script_details.tbody.contents[2].find(string="Average user rating").next_element.next_element.next_element.next_element.replace(' (','')[0:3]
#             author_start = script_details.tbody.contents[2].find(string="Writers")
#             authors = []
#             next = author_start.next_element
#             while next.name != 'b':
#                 if next.name == 'a':
#                     authors.append(next.text)
#                 next = next.next_element
#             separator = ', '
#             authors = separator.join(authors)

#             genres_start = script_details.tbody.contents[2].find(string="Genres")
#             genres = []
#             next = genres_start.next_element
#             while next.name != 'b':
#                 if next.name == 'a':
#                     genres.append(next.text)
#                 next = next.next_element

#             genres = separator.join(genres)

#             if script_details.tbody.contents[2].find(string="Script Date"):
#                 date = script_details.tbody.contents[2].find(string="Script Date").next_element.replace(' : ','')
#             else:
#                 date = "NULL"

#             movie.title = title
#             movie.rating = rating
#             movie.authors = authors
#             movie.genres = genres
#             movie.date = date

#             # SCRAPE AND LOAD SCRIPT TEXT
#             URL_SCRIPT = "https://www.imsdb.com/scripts/" + i_script + ".html"
#             rs = requests.get(URL_SCRIPT, timeout = timeout) 
#             if r.status_code == 200:
#                 print("script_success")
#             else:
#                 print("fscript_ailure")            
#             if (rs.status_code == 200):
#                 soup_2 = BeautifulSoup(rs.content, 'html5lib')

#                 if soup_2.find('td', attrs = {'class':'scrtext'}):
#                     script = soup_2.find('td', attrs = {'class':'scrtext'}).text.strip().replace("\n","")

#                     movie.script = script

#                     # APPEND MOVIE OBJECT
#                     movies.append(movie)

# # SAVE INTO SCV
# import csv
# with open('data.csv', 'w',) as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['title', 'rating', 'authors', 'genres', 'date', 'script'])
#     for movie in movies:
#         writer.writerow([movie.title, movie.rating, movie.authors, movie.genres, movie.date, movie.script]) 

