#!/usr/bin/env python3
import requests as re
from bs4 import BeautifulSoup as bs
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

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
dirname = '/home/ubuntu/' + now.strftime('%Y-%m-%d' + '-pdf') 
os.system('sudo mkdir {}'.format(dirname))
filepath = dirname + '/' + filename
with open(filepath, 'wb') as f:
	content = re.get(file_url, verify=False).content
	f.write(content)

msg = MIMEMultipart()
msg['To'] = "foo@example.com"
msg['From'] = "update@scraper.com"
msg['Subject'] = "Test Report"

body = MIMEText('Dear user; this is a test.', 'plain', 'utf-8')
msg.attach(body)  # add message body (text or html)
attachment = MIMEApplication(content, _subtype="xlsx")
attachment.add_header('Content-Disposition','attachment', filename=filename)
msg.attach(attachment)

# Send the email
with smtplib.SMTP('smtp.example.com', 25) as server:
    server.starttls()  # Secure the connection
    server.login('update@scraper.com', 'password')
    server.sendmail(msg['From'], msg['To'], msg.as_string())
