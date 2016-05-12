from bs4 import BeautifulSoup # documentation available at : #www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import NavigableString, Tag
import requests # To send http requests and access the page : docs.python-requests.org/en/latest/
import csv # To create the output csv file
import unicodedata # To work with the string encoding of the data
import urllib
import re

def crawlPage(urlToCrawl):

	print "I am going to crawl at:  "+urlToCrawl


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

	if len(urlToCrawl) > 0:
		url = urlToCrawl

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
	camps = soup.find_all("div", class_="campListing featuredCamp")
	#print camps
	#print "-------------------------------"

	#info = soup.find_all("div", style="display:none")
	#print info

	entry = ["stree-address", "locality", "Camp Name", "Contact Name", "Email", "Phone Number"]
	entries.append(entry)

	for element in camps:
	    entry = []
	    targetDiv = element.find("div", class_="location vcard")
	    orgName = ""
	    tempStr = targetDiv.a.get_text()

	    print "I found this location: " + tempStr;

	    return

	    # The encoding is because the format exracted is a unicode. We need a uniform structure to work with the strings.
	    orgName = (orgName + ' '+ tempStr.encode('iso-8859-1')).strip()
	    entry.append(orgName)
	    entry.append(targetDiv.a["href"])
	    
	    targetDiv = element.find("div", class_="adr")
	    campName = ""
	    tempStr = targetDiv.get_text()
	    # The encoding is because the format exracted is a unicode. We need a uniform structure to work with the strings.
	    campName = (campName + ' '+ tempStr.encode('iso-8859-1')).strip()
	    entry.append(campName)
	    
	    #some camps do not have a section that lists the contact, email and phoneNo info
	    #if the targetDiv has a p-tag, then we can grab the data
	    targetDiv = element.find("div", id=re.compile("camp(\d+)details"))
	    targetP = targetDiv.find("p") #use "find" because "find_all" returns a list instead of an element
	    
	    #while targetP is None and i < 10:
	    #   if targetDiv.next_sibling:
	    #      targetP = targetDiv.next_sibling.find("p")
	    
	    if targetP:
		if debug:
		    print "----------targetP--------------------"
		    print targetP
		    print "-------------------------------------------"
		
		#check for None because some targetP's only have a phone number and no other contents
		if targetP.contents is not None and len(targetP.contents) > 2:
		    contactName = ""
		    tempStr = targetP.contents[2] #3rd element in contents contains the name of Director, everything else is jumbled together
		    contactName = (contactName + ' '+ tempStr.encode('iso-8859-1')).strip()
		    entry.append(contactName)
		    
		    if targetP.a is not None:
			emailAddr = ""
			tempStr = targetP.a.get_text()
			emailAddr = (emailAddr + ' '+ tempStr.encode('iso-8859-1')).strip()
			entry.append(emailAddr)
			
			if targetP.a.next_sibling is not None:
			    phoneNum = ""
			    tempStr = targetP.a.next_sibling.get_text()
			    phoneNum = (phoneNum + ' '+ tempStr.encode('iso-8859-1')).strip()
			    entry.append(phoneNum)
	    #only add a phone number to the entry, leave others blank
	    else:
		entry.append("") #empty contactName
		entry.append("") #empty emailAddr
		entry.append(targetP.get_text())



	if debug:
	    print "-------------------------------------------"
	    print "adding entry %d:" % (i)
	    print entry
	    print "-------------------------------------------"
	    entries.append(entry)
	    i += 1


	with open('classes_target_list.csv', 'w') as output:
	    writer = csv.writer(output, delimiter= ',', lineterminator = '\n')
	    writer.writerows(entries)
	print "Wrote to classes_target_list.csv"

