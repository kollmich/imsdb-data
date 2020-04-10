try: 
    import requests 
    from requests.exceptions import HTTPError
    import os
    import html5lib
    from bs4 import BeautifulSoup 
    import re
    import json
    import urllib.request
    from urllib.parse import urlparse
    from urllib import parse
    #from sys import argv
    import sys 
    # reload(sys)
    # sys.setdefaultencoding('utf8')
    import shutil
    import time
    import zipfile
    import pysrt
    import json
    import string
except: 
    print("Libraries not found.") 
    sys.exit()


movies = []
movies_list = []

### DEFINE FUNCTION TO ITERATE THROUGH THE MOVIES LIST, GET INFO, FIND & PROCESS SUBTITLES, SAVE AS A SINGLE DATASET
## GET MOVIE INFO
def get_movie_data(movies_list):
    # INIT OBJECT

    for i in movies_list:
        class movie(object):
            def __init__(self):
                self.title = ""
                self.year = ""
                self.rating= ""
                self.subtitles= ""
            def __repr__(self):
                return str(self)
        # h2 = i.find('div', attrs = {'class':'article_movie_title'})
        # title = h2.a.text.strip()
        # year = h2.find('span', attrs = {'class':"subtle start-year"}).text.strip()

        # actors = []
        # actors_div = i.find('div', attrs = {'class':'info cast'}).findAll('a')
        # for j in actors_div:
        #     actor = j.text
        #     actors.append(actor)
        # separator = ', '
        # actors = separator.join(actors)

        # director = i.find('div', attrs = {'class':"info director"}).a.text.strip()

        movie.title = i
        # movie.year = '1991' #year.replace('(','').replace(')','')
        # movie.rating = rating.replace('%','')
        # movie.actors = actors
        # movie.director = director

        ## SCRAPE AND LOAD SUBTITLES
        url = "http://www.yifysubtitles.com/search?q=" 
        movie_name = movie.title
        movie_fix = movie_name.lower().replace("½"," 1/2").replace("é","e").replace(" ", "+")

        # connect to url
        movie_url = url + movie_fix

        scheme, netloc, path, query, fragment = parse.urlsplit(movie_url)
        path = parse.quote(path)
        movie_url = parse.urlunsplit((scheme, netloc, path, query, fragment))
        print(movie_url)

        try:
            source = urllib.request.urlopen(movie_url).read() 
            soup_movie = BeautifulSoup(source, "html.parser", from_encoding="utf-8") 
        except urllib.error.HTTPError:
            print('MISSING SEARCH', movie_name)
            pass
        # Searches through a table of movies
        if soup_movie.find("h3", string = movie.title):
            link = soup_movie.find("h3", string = movie.title).find_parent("a").get("href") 
            #print(link)
            parse_obj = urlparse(movie_url)
            url = parse_obj.scheme + "://" + parse_obj.netloc 
            sub_url = url + link 

            try:
                sub_source = urllib.request.urlopen(sub_url).read() 
                soup_sub = BeautifulSoup(sub_source, "html.parser",from_encoding="utf-8")

            except urllib.error.HTTPError:
                print('MISSING PAGE', movie_name)
                pass
                
            # Searches through a list of subtitles
            if soup_sub.find("span", string = "English"):
                yify = "https://www.yifysubtitles.com/"
                year = soup_sub.find('div', attrs = {'class':"circle", 'data-info':"year"}).get("data-text")
                rating = soup_sub.find('div', attrs = {'class':"circle", 'data-info':"Tomato"}).get("data-text")
                link_sub = soup_sub.find("span", string = "English").find_parent("tr").find("a", {"class":"subtitle-download"}).get("href")
                link_sub = yify + link_sub
                #print(link_sub)
                sub_final = urllib.request.urlopen(link_sub).read() 
                soup_final = BeautifulSoup(sub_final, "html.parser",from_encoding="utf-8")

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
                            try:
                                f.extract(file, path = 'subs') 
                                subs = pysrt.open(os.path.join(dest, file), encoding='iso-8859-1')
                                file_name = '{}/{}.txt'.format(dest, movie.title)
                                try:
                                    os.remove(file_name)
                                except:
                                    print("Error while deleting file ", file_name)

                                if subs:
                                    for sub in subs:
                                        with open(file_name, 'a') as f:
                                            #f.write("1\n")
                                            #f.write("{0} --> {1}\n".format(start_new, end_new))
                                            f.write(sub.text)
                                            #movie.subtitles = sub_text
                                    with open(file_name) as fp:
                                        subtitles = fp.read()
                                else:
                                    print("Error while writing file ", file)                           
                                    subtitles = "no link"                                    
                            except:
                                print("Error while extracting file ", file)                           
                                subtitles = "no link"        
                        else:
                            subtitles = "no link"
                else:
                    subtitles = "no link"
            else:
                subtitles = "no link"      
        else:
            subtitles = "no link"

        movie.subtitles = subtitles
        if year is None:
            movie.year = "N/A"
        else:
            movie.year = year
        if rating is None:
            movie.rating = "N/A"
        else:
            movie.rating = rating

        print(movie.title, movie.year, movie.rating)

        movies.append(movie)

URL1 = "https://www.boxofficemojo.com/chart/top_lifetime_gross_adjusted/?adjust_gross_to=2020"
URL2 = "https://www.boxofficemojo.com/chart/top_lifetime_gross_adjusted/?adjust_gross_to=2020&offset=200"
URL3 = "https://www.boxofficemojo.com/chart/top_lifetime_gross_adjusted/?adjust_gross_to=2020&offset=400"
URL4 = "https://www.boxofficemojo.com/chart/top_lifetime_gross_adjusted/?adjust_gross_to=2020&offset=600"
URL5 = "https://www.boxofficemojo.com/chart/top_lifetime_gross_adjusted/?adjust_gross_to=2020&offset=800"

urls = [URL1, URL2, URL3, URL4, URL5]

for u in urls:
    req = requests.get(u)
    soup = BeautifulSoup(req.content, 'html5lib', from_encoding="utf-8")
    links = soup.findAll('td', attrs = {'class':'a-text-left mojo-field-type-title'})
    for t in links:
        title = t.find('a', attrs = {'class':'a-link-normal'}).text.strip()
        movies_list.append(title.replace("·", " ").replace("/"," "))

print(movies_list)
get_movie_data(movies_list)

movies_json = [{"title": movie.title, 
                "year": movie.year,
                "rating": movie.rating,
                #"actors": movie.actors,
                #"director": movie.director,
                "subtitles": movie.subtitles.translate(str.maketrans('', '', string.punctuation)).replace("\n"," ").replace("."," ").lower()}
                for movie in movies]

with open('output/data.txt', 'w') as outfile:
    json.dump(movies_json, outfile)

for srt in os.scandir('{}/{}'.format(os.getcwd(), 'subs')):
    if srt.name.endswith(".srt"):
        os.unlink(srt.path)

