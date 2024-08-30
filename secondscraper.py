#!/usr/bin/env python3
import requests as re
from bs4 import BeautifulSoup as bs


#url = "https://anpp.dz/textes-reglementaires-pp/"
url = 'https://anpp.dz/textes-reglementaires-dm/'
response = re.get(url, verify=False).content
soup = bs(response, 'html.parser')

new_reg = soup.find('h6').find('a')
print("announcement", new_reg.text)
file_url = new_reg.get('href')
print(file_url)
#filename = file_url.split('#')[0].split('/')[-1]
filename = file_url.split('?')[0].split('/')[-1]
page_number = file_url.split('#')[-1]
journal_numner = file_url.split('?')[-1].split('#')[0]
print('modification occurs at page', page_number)
print('journal number', journal_numner)
with open(filename, 'wb') as f:
	content = re.get(file_url, verify=False).content
	f.write(content)


# for title in titles:
# 	if title.string is None:
# 		continue
# 	else:
# 		if "nomenclature" in title.string.lower():
# 			h3 = title
# file_url = h3.parent.next_sibling.next_sibling.find('a').get('href')
# print(file_url)
# filename = file_url.split('/')[-1]
# with open(filename, 'wb') as f:
# 	content = re.get(file_url, verify=False).content
# 	f.write(content)

