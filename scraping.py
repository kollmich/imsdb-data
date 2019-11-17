import requests 
import html5lib
from bs4 import BeautifulSoup 

URL = "https://www.imsdb.com/Movie%20Scripts/Jackie%20Brown%20Script.html"
r = requests.get(URL) 

soup = BeautifulSoup(r.content, 'html5lib') 

title = soup.find('table', attrs = {'class':'script-details'}).find('h1')

print(title.text)


