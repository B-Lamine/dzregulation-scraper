#!/usr/bin/env python3
import requests as re
from bs4 import BeautifulSoup as bs
import os
import sys
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

dbcursor.execute("SELECT username, pwd, host FROM credentials")
login = list(dbcursor.fetchone())
db.close()

# dirname = 'pdf' + now.strftime('%Y%m%d%H%M%S') # '/home/ubuntu/' +
# os.system('sudo mkdir storage/{}'.format(dirname))
# filepath = 'storage/' + dirname + '/' + filename
# with open(filepath, 'wb') as f:
# 	content = re.get(file_url, verify=False).content
# 	f.write(content)

#msg = EmailMessage()
msg = MIMEMultipart()
msg['To'] = sys.argv[1]
msg['From'] = login[0]
msg['Subject'] = "Test Report"

body = MIMEText('Dear user; this is a test.', 'plain', 'utf-8')
msg.attach(body)  # add message body (text or html)

#attachment = MIMEApplication(content, _subtype="xlsx")
#attachment.add_header('Content-Disposition','attachment', filename=filename)
#msg.attach(attachment)


# Send the email
with smtplib.SMTP(login[2], 25) as server:
#    server.set_debuglevel(1)
    error, message = server.verify(str(sys.argv[1]))
    print('error', error, 'message :', message)
    server.starttls()  # Secure the connection
    server.login(login[0], login[1])
    print('\n#############\n', list(server.__dict__.keys()),'\n################\n')
# print(server.ehlo_resp)
    error, message = server.verify(str(sys.argv[1]))
    print('error', error, 'message :', message)
    try:
        server.sendmail(msg['From'], msg['To'], msg.as_string())
    except Exception as e:
        print(e)
