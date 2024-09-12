#!/usr/bin/env python3
from bs4 import BeautifulSoup as bs
from datetime import datetime
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import mysql.connector
import os
import requests as re
import smtplib

db = mysql.connector.connect(
  host="localhost",
  user="portfoo",
  password="portfoo_pwd",
  database="portfoo_db"
)
dbcursor = db.cursor()

dbcursor.execute("SELECT name, email FROM mailing_list")
data = [list(el) for el in dbcursor.fetchall()]
mailing_list = [el[1] for el in data]

dbcursor.execute("SELECT username, pwd, host FROM credentials")
login = list(dbcursor.fetchone())
db.close()

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
filename = file_url.split('/')[-1]
now = datetime.now()
dirname = 'pdf' + now.strftime('%Y%m%d%H%M%S')
os.system('sudo mkdir app/storage/{}'.format(dirname))
filepath = 'app/storage/' + dirname + '/' + filename
with open(filepath, 'wb') as f:
	content = re.get(file_url, verify=False).content
	f.write(content)

msg = MIMEMultipart()
msg['To'] = ", ".join(mailing_list)
msg['From'] = login[0]
msg['Subject'] = "Test Report"

body = MIMEText('Dear user; this is a test.', 'plain', 'utf-8')
msg.attach(body)
attachment = MIMEApplication(content, _subtype="xlsx")
attachment.add_header('Content-Disposition','attachment', filename=filename)
msg.attach(attachment)

with smtplib.SMTP(login[2], 25) as server:
    server.starttls()
    server.login(login[0], login[1])
    server.sendmail(msg['From'], mailing_list, msg.as_string())
