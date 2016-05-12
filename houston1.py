from bs4 import BeautifulSoup # documentation available at : #www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import NavigableString, Tag
import requests # To send http requests and access the page : docs.python-requests.org/en/latest/
from crawl import crawlPage #local webpage crawler
import csv # To create the output csv file
import unicodedata # To work with the string encoding of the data
import urllib
import re
import subprocess

entries = []
entry = []
i = 1
debug = True
data = ""
r = ""
#the url of the page we want to parse
url="http://houston.kidsoutandabout.com/content/top-20-places-take-kids-houston-area"
#url = "http://localhost/analytics/nmc-classes.html"
if debug:
    print "processing url: " + url
    print "--------------------------------"


try:
    r = requests.get(url, timeout = 10) #Sending a request to access the page
    data = r.text
except Exception,e:
    print "Error: exception thrown trying to access the url!"

#print data
#print "---------------------------------"

soup = BeautifulSoup(data, "html.parser") # Getting the page source into the soup
#print soup.prettify()[0:500]

#get all the ..
camps = soup.find_all("a",href=True, target="_blank")
print "camps found are:  "

i = 1
for camps_found in camps:
	if "uston.kidsoutandabout.com/content/" in camps_found['href']:
		print ("{} {}".format(i,camps_found['href']))
		i = i+1
		#call crawler
		crawlPage(camps_found['href'])

