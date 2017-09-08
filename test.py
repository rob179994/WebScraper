# -*- coding: utf-8 -*-

import sys
import webbrowser
import requests
import time
import selenium.webdriver as webdriver
import re
import random
import io


# Extract word to search from argument
word_to_search=str('site:'+sys.argv[1])
searchResults = 1


#Open and write to file
with io.FileIO("Web_Scraper_Sites.txt", "a") as file:
    file.write("\n \n \n \n")
    file.write("Web scraping started. Input: " + "'" + sys.argv[1] + "'")



# optional number of iterations
iterations =1
iterate = False
try:
	iterations = int(sys.argv[2])
	iterate = True
	with io.FileIO("Web_Scraper_Sites.txt", "a") as file:
		file.write(". Iterations: " + iterations)
except:
	print('no iteration selected!')
	with io.FileIO("Web_Scraper_Sites.txt", "a") as file:
		file.write(". No iteration limit")

with io.FileIO("Web_Scraper_Sites.txt", "a") as file:
    file.write("\n \t Current date "  + time.strftime("%x"))
    file.write("\n \t Current time " + time.strftime("%X"))
    file.write("\n\nRemoved URLs:")

# repeat until no results are left
removedStrings = []
while (searchResults>0):

	if (iterate == True):
		if (iterations==0):
			break

	# send request for specific page
	links = []
	request = requests.get('http://google.com/search?q='+word_to_search)
	content=request.content.decode('UTF-8','replace')	
	
	# find number of results
	
	searchResultsValue = re.search('id="resultStats">About (.+?) results</div>', content)

	try:
		searchResultsString = searchResultsValue.group(1) 
	except:
		print('Error, request did not work. You may not be connected to the internet or CAPTCHA...')
		#print(content)
		break
	
	searchResultsString = searchResultsString.replace(",","")
	searchResults = int(searchResultsString)
	
	# NEED TO IMPROVE THIS
	while '<h3 class="r">' in content:
		content=content.split('<h3 class="r">', 1)[1]
		split_content=content.split('</h3>', 1)

		try:
			link='http'+split_content[1].split(':http',1)[1].split('%',1)[0]
		except:
			print('This link has no http protocol')
			continue

		link = link.replace("http://","",1)
		link = link.replace("https://","",1)
		links.append(link)
		content=split_content[1]
		break
	
	print('Length of list: ' + str(len(links)))
	removedStrings.append(links[0])
	word_to_search = word_to_search + ' -site:' + links[0]

	with io.FileIO("Web_Scraper_Sites.txt", "a") as file:
		file.write("\n \t -" + "'" + links[0] + "'")

	
	time.sleep(3+random.random())
	print('New word to search: '+word_to_search)
	print(searchResults)
	
	if (iterate == True):
		iterations -=1
	
print("\nREMOVED STRINGS:")
print(removedStrings)
print("\n\n")
