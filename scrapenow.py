#!/usr/bin/env python3
import requests as re
from bs4 import BeautifulSoup as bs
import os
from datetime import datetime


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
print(h3.parent.next_sibling.next_sibling.next_sibling.next_sibling.find('a').get('href'))
exit()

file_url = h3.parent.next_sibling.next_sibling.find('a').get('href')
#print(file_url)
filename = file_url.split('/')[-1]
now = datetime.now()
dirname = 'pdf' + now.strftime('%Y%m%d%H%M%S') # '/home/ubuntu/' +
os.system('sudo mkdir app/storage/{}'.format(dirname))
filepath = 'app/storage/' + dirname + '/' + filename
with open(filepath, 'wb') as f:
	content = re.get(file_url, verify=False).content
	f.write(content)
