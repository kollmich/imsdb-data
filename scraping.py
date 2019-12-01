try: 
    import requests 
    import os
    import html5lib
    from bs4 import BeautifulSoup 
    import re
    import json
    import urllib.request
    from urllib.parse import urlparse 
    #from sys import argv
    import sys 
    import shutil
    import time
    import zipfile
    import srt_to_txt
except: 
    print("Libraries not found.") 
    sys.exit()

#timeout = 100

# GET LIST OF ALL OSCAR-WINNING MOVIES
URL_ROTTEN_1 = "https://editorial.rottentomatoes.com/guide/oscars-best-and-worst-best-pictures/"
URL_ROTTEN_2 = "https://editorial.rottentomatoes.com/guide/oscars-best-and-worst-best-pictures/2/"

rot_1 = requests.get(URL_ROTTEN_1) 
rot_2 = requests.get(URL_ROTTEN_2) 

soup_01 = BeautifulSoup(rot_1.content, 'html5lib') 
soup_02 = BeautifulSoup(rot_2.content, 'html5lib') 

movies = []


### ITERATE THROUGH THE MOVIES LIST, GET INFO, FIND & PROCESS SUBTITLES, SAVE AS A SINGLE DATASET
## GET MOVIE INFO
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

    # # SCRAPE AND LOAD SUBTITLES
    url = "http://www.yifysubtitles.com/search?q=" 
    movie_name = movie.title 
    movie_fix = movie_name.lower().replace(" ", "+") 

    # connect to url
    movie_url = url + movie_fix 
    source = urllib.request.urlopen(movie_url).read() 
    soup_movie = BeautifulSoup(source, "html.parser") 

    # Searches through a table of movies
    if soup_movie.find("h3", string = movie.title):
        link = soup_movie.find("h3", string = movie.title).find_parent("a").get("href") 
        print(link)
        parse_obj = urlparse(movie_url) 
        url = parse_obj.scheme + "://" + parse_obj.netloc 
        sub_url = url + link 

        sub_source = urllib.request.urlopen(sub_url).read() 
        soup_sub = BeautifulSoup(sub_source, "html.parser") 

        # Searches through a list of subtitles
        if soup_sub.find("span", string = "English"):
            yify = "https://www.yifysubtitles.com/"
            link_sub = soup_sub.find("span", string = "English").find_parent("tr").find("a", {"class":"subtitle-download"}).get("href")
            link_sub = yify + link_sub
            print(link_sub)
            sub_final = urllib.request.urlopen(link_sub).read() 
            soup_final = BeautifulSoup(sub_final, "html.parser") 

            # Scrapes the subtitle url
            if soup_final.find("a", {"class":"btn-icon download-subtitle"}):
                link_final = soup_final.find("a", {"class":"btn-icon download-subtitle"}).get("href")
                print(link_final)                
                
                current_directory = os.getcwd()
                zip_directory = os.path.join(current_directory, r'zip')
                if not os.path.exists(zip_directory):
                    os.makedirs(zip_directory)                
                urllib.request.urlretrieve(link_final, '{}/{}.zip'.format(zip_directory, movie.title))
                zip_file = '{}/{}.zip'.format(zip_directory, movie.title)
                dest = os.path.join(current_directory, r'subs')
                if not os.path.exists(dest):
                    os.makedirs(dest)
                f = zipfile.ZipFile(zip_file)


                for file in f.namelist(): 
                    if file.endswith('.srt'): 
                        print('Extracting: ' + file)
                        f.extract(file, path = 'subs') 
                        time.sleep(2)
                        # subs = '{}/{}.srt'.format(dest, movie.title)

                        # srt_to_txt.main(subs)
                        """
                        NOTES
                        * Run from command line as
                        ** python srt_to_txt.py file_name.srt cp1252
                        * Creates file_name.txt with extracted text from file_name.srt 
                        * Script assumes that lines beginning with lowercase letters or commas 
                        * are part of the previous line and lines beginning with any other character
                        * are new lines. This won't always be correct. 
                        """

                

            else:
                link_final = "no link"

        else:
            link_final = "no link"
        
    else:
        link_final = "no link"


    movie.link_final = link_final

    print(movie.title, movie.year, movie.rating, movie.actors, movie.director, movie.link_final)

    movies.append(movie)




divs_01 = soup_01.findAll('div', attrs = {'class':'col-sm-18 col-full-xs countdown-item-content'})
for i in divs_01:
    get_movie_data(movies)

divs_02 = soup_02.findAll('div', attrs = {'class':'col-sm-18 col-full-xs countdown-item-content'})
for i in divs_02:
    get_movie_data(movies)


# SAVE INTO CSV
import csv
with open('data.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['title', 'year', 'rating', 'actors', 'director', 'script', 'link_final'])
    for movie in movies:
        writer.writerow([movie.title, movie.year, movie.rating, movie.actors, movie.director, movie.link_final]) 

