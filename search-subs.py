# SCRIPT BY NoahG07 from https://github.com/NoahG07/Python-Subtitle-Scraper
#! /usr/bin/env python3 
#
# This script allows you to search YIFY Subtitles 
# Importing needed libraries
try: 
    import urllib.request 
    from urllib.parse import urlparse 
    #from sys import argv
    import sys 
    import bs4 as bs 
except: 
    print("Libraries not found.") 
    sys.exit()


# entering 'movie name' into url 
url = "http://www.yifysubtitles.com/search?q=" 
movie_name = input("[*] Search for: ")  
movie_fix = movie_name.lower().replace(" ", "+") 

# Getting connection to website
movie_url = url + movie_fix 
source = urllib.request.urlopen(movie_url).read() 
soup = bs.BeautifulSoup(source, "html.parser") 

# Counting the number of results
count = 0

# Searches through a table of movies
tables = soup.findAll("li", {"class": "media media-movie-clickable"}) 
for table in tables: 

    # Goes to media-body of the container
    media_body = table.findAll("div", {"class":"media-body"}) 
    media_body = media_body[0] 

    # Finding movie subtitle URL
    # finds movie/subtitle sub-link 
    sub_link = media_body.findAll("a") 
    sub_link = sub_link[0] 
    link = sub_link.get("href") 

    # parses the original url 
    parse_obj = urlparse(movie_url) 
    url = parse_obj.scheme + "://" + parse_obj.netloc 
    sub_url = url + link 

    # Finds the movie title
    movie_title = media_body.findAll("h3", {"itemprop":"name"}) 
    movie_title = movie_title[0] 
    title = movie_title.string 

    # Finds the year of the movie
    years = media_body.findAll("span", {"class":"movinfo-section"})[0] 
    year = years.contents[0]

    count += 1
    # Prints to the user the Movie-Year and URL
    print(str(count) + ") " + title + " (" + year + ")" + "\n" + sub_url + "\n")