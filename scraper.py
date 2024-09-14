#!/usr/bin/env python3
import requests as re
from bs4 import BeautifulSoup as bs
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import mysql.connector

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
#db.commit()

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
file_url = h3.parent.next_sibling.next_sibling.next_sibling.next_sibling.find('a').get('href')
#print(file_url)
filename = file_url.split('/')[-1]
now = datetime.now()
#dirname = 'pdf' + now.strftime('%Y%m%d%H%M%S') # '/home/ubuntu/' +
#os.system('sudo mkdir app/storage/{}'.format(dirname))
filepath = 'app/storage/' + filename # + dirname + '/'
with open(filepath, 'wb') as f:
	content = re.get(file_url, verify=False).content
	f.write(content)

#msg = EmailMessage()
msg = MIMEMultipart()
msg['To'] = ", ".join(mailing_list)
msg['From'] = login[0]
msg['Subject'] = "Update Report"

body = MIMEText('Dear user; Please find attached the latest updates.', 'plain', 'utf-8')
#body = 'Dear user; this is a test.'
msg.attach(body)  # add message body (text or html)
files = os.popen('ls app/storage/').read()[:-1].split('\n')

for f in files:  # add files to the message
        file_path = os.path.join('app/storage/', f)
        attachment = MIMEApplication(open(file_path, "rb").read(), _subtype=f.split('.')[-1])
        attachment.add_header('Content-Disposition','attachment', filename=f)
        msg.attach(attachment)

# attachment = MIMEApplication(content, _subtype="xlsx")
# attachment.add_header('Content-Disposition','attachment', filename=filename)
# msg.attach(attachment)

# Send the email
with smtplib.SMTP(login[2], 25) as server:
    server.starttls()  # Secure the connection
    server.login(login[0], login[1])
    server.sendmail(msg['From'], mailing_list, msg.as_string())
