#!/usr/bin/env python3
import requests as re
from bs4 import BeautifulSoup as bs
import os
from datetime import datetime

#response = re.get('https://web-scraping.dev/login').content
#soup = bs(response, 'html.parser')
#atags = soup.find_all('a')
#for a in atags:
#	if '.pdf' in a.get('href'):
#		file = re.get(a.get('href')).content
#		filename = a.get('href').split('/')[-1]
#		with open(filename, 'wb') as f:
#			f.write(file)

url = "http://www.miph.gov.dz/fr/telechargements/"
response = re.get(url, verify=False).content
soup = bs(response, 'html.parser')

titles = soup.find_all('strong')

for title in titles:
	if title.string is None:
		continue
	else:
		if "nomenclature" in title.string.lower():
			h3 = title
file_url = h3.parent.next_sibling.next_sibling.find('a').get('href')
#print(file_url)
filename = file_url.split('/')[-1]
now = datetime.now()
dirname = now.strftime('%Y-%m-%d' + '-pdf')
os.system('mkdir {}'.format(dirname))
with open(dirname + '/' + filename, 'wb') as f:
	content = re.get(file_url, verify=False).content
	f.write(content)
