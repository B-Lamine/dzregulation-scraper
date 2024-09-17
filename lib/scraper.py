#!/usr/bin/env python3
"""
Scraper functionalities
"""


from bs4 import BeautifulSoup as bs
from datetime import datetime
import os
import requests as re


def get_link(url):
	"""
	the webpage of the url is parsed and search for the file url
	"""
	# get and parse html page
	#url = "http://www.miph.gov.dz/fr/telechargements/"
	response = re.get(url, verify=False).content
	soup = bs(response, 'html.parser')
	# get all strong tags
	titles = soup.find_all('strong')
	# go through all titles and stop at "nomenclatature"
	for title in titles:
		if title.string is None:
			continue
		else:
			if "nomenclature" in title.string.lower():
				h3 = title
	# get the download link to the file
	file_url = h3.parent.next_sibling.next_sibling.next_sibling.next_sibling.find('a').get('href')
	return file_url

def download_file(file_url):
	"""
	Save file whose url is passed to app's storage;
	return filepath
	"""
	filename = file_url.split('/')[-1]
	# save file to storake directory of the app
	filepath = 'app/storage/' + filename
	with open(filepath, 'wb') as f:
		content = re.get(file_url, verify=False).content
		f.write(content)
	return filepath
