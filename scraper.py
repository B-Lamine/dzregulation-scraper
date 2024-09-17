#!/usr/bin/env python3


from bs4 import BeautifulSoup as bs
from datetime import datetime
from email.message import EmailMessage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mysql.connector
import os
import requests as re
import smtplib


# connect to database
db = mysql.connector.connect(
  host="localhost",
  user="portfoo",
  password="portfoo_pwd",
  database="portfoo_db"
)
# instantiate a cursor to the database
dbcursor = db.cursor()
# get subscribers email addresses
dbcursor.execute("SELECT name, email FROM mailing_list")
data = [list(el) for el in dbcursor.fetchall()]
mailing_list = [el[1] for el in data]
# get login info to websites email service
dbcursor.execute("SELECT username, pwd, host FROM credentials")
login = list(dbcursor.fetchone())
db.close()

# get and parse html page
url = "http://www.miph.gov.dz/fr/telechargements/"
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
filename = file_url.split('/')[-1]
# save file to storake directory of the app
filepath = 'app/storage/' + filename
with open(filepath, 'wb') as f:
	content = re.get(file_url, verify=False).content
	f.write(content)

# instantiate an email object headers
msg = MIMEMultipart()
msg['To'] = ", ".join(mailing_list)
msg['From'] = login[0]
msg['Subject'] = "Update Report"
# set email text
body = MIMEText('Dear user; Please find attached the latest updates.', 'plain', 'utf-8')
msg.attach(body)  # add message body (text or html)
files = os.popen('ls app/storage/').read()[:-1].split('\n')
# get all files in storage and attach them to email
for f in files:
        file_path = os.path.join('app/storage/', f)
        attachment = MIMEApplication(open(file_path, "rb").read(), _subtype=f.split('.')[-1])
        attachment.add_header('Content-Disposition','attachment', filename=f)
        msg.attach(attachment)


# Send the email
with smtplib.SMTP(login[2], 25) as server:
    server.starttls()  # Secure the connection
    server.login(login[0], login[1])
    server.sendmail(msg['From'], mailing_list, msg.as_string())
