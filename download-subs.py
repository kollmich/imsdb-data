# SCRIPT BY NoahG07 from https://github.com/NoahG07/Python-Subtitle-Scraper
#! /usr/bin/env python3 
#
# This Script Lets You Download Subtitles 
# In Your Language From YIFY Subtitles

# Imports The Needed Libraries
try: 
    from urllib.parse import urlparse
    from sys import argv 
    import bs4 as bs 
    import urllib.request 
    import getpass
    import subprocess, os, time
except: 
    print("Libraries not found.")

# Takes The Script and URL As Arguments
try: 
    script, my_url = argv 
except ValueError: 
    print("URL not found.")
    exit

# Variable For The Logged In User
user = getpass.getuser()
# Goes To Users Downloads Folder
os.chdir("/home/{}/Downloads/".format(user))

# Opens The YIFY Subtitle Website To Be Read
#my_url = input("Enter url: ")
source = urllib.request.urlopen(my_url).read() 
soup = bs.BeautifulSoup(source, "html.parser") 

# Gets Movie Name
title_sub = soup.title.string

# Variable for Subtitle Table
table_subs = soup.find("table", {"class":"table other-subs"}).findAll("tr")

# The First List In The Table Is Useless
useless = table_subs.pop(0)

# Makes A List For The English Rows
tabs = []

# Searches Through The Tabe For The First English Subtitles.
# Just edit this top piece of code to download a language 
# other than English.
for table in table_subs:
    if table.find("span", {"class":"sub-lang"}).string == "English":
        tabs.append(table)

        # Uses The First Subtitle Class Because It IS The Highest Rating Subtitle
        my_subs = tabs[0]
        
        # Finds The Subtitle URL
        sub_link = my_subs.findAll("a")[0]
        #sub_link = sub_link[0]
        link = sub_link.get("href")
        
        # Makes A Variable For The Subtitle URL
        parse_obj = urlparse(my_url)
        url = parse_obj.scheme + "://" + parse_obj.netloc
        sub_url = url + link
        
        # Opens The Subtitle URL To Be Read
        source = urllib.request.urlopen(sub_url).read()
        soup = bs.BeautifulSoup(source, "html.parser")
        
        # Variable For The Zip URL
        zip_url = soup.findAll("a", {"class":"btn-icon download-subtitle"})
        z_url = zip_url[0]
        file = z_url.get("href")
        
        # Parses ONLY The File/Movie Name NOT The URL
        movie_url = urlparse(file)
        movie_path = movie_url.path
        movie = movie_path.replace("/subtitle/", "")
        # If Subtitles Are Already On System Ignore, If Not Download
        # The File
        if os.path.isfile(movie):
            print(movie + ": Already Exists on Filesystem")
            exit
        else:
            # Downloads The Zip URL
            try:
                print("Downloading... " + title_sub)
                time.sleep(2)
                subprocess.Popen(["wget", file])
                break
            except:
                print("[*]ERROR: Failed to Download\n" + file)