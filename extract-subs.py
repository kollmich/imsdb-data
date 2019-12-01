# SCRIPT BY NoahG07 from https://github.com/NoahG07/Python-Subtitle-Scraper
#! /usr/bin/env python3 
# 
# This script searches and extracts subtitles from zip folders

import os, zipfile, shutil, time, getpass

# gets username
user = getpass.getuser() 


# import os
# print(os.path.expanduser('~'))

# users download directory
home = '/Users/{}/Downloads'.format(user)

os.chdir(home) 

try:
    dest = '/Users/{}/Downloads/movie_subs'.format(user) 
    os.mkdir(dest) 
except FileExistsError:
    print('Directory Exists: movie_subs/\n')

dest = '⁨/Users/{}/Downloads/movie_subs/'.format(user)

for f in os.listdir(): 
    if f.endswith('.zip'): 
        f = zipfile.ZipFile(f) 
        for file in f.namelist(): 
            if file.endswith('.srt'): 
                print('Extracting: ' + file)
                f.extractall(file) 
                time.sleep(2)
                shutil.move(file, dest)