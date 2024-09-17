#!/usr/bin/env python3
"""
Email functionalities
"""


from email.message import EmailMessage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib


def send_email(recipient, login:list, subject, body):
	"""
	Send emails to subscribers
	returns error code, and accompanying error if one occurs
	otherwise returns None
	"""
	# instantiate an email object headers
	msg = MIMEMultipart()
	msg['To'] = recipient
	msg['From'] = login[0]
	msg['Subject'] = subject
	# set email text
	body = MIMEText(body, 'plain', 'utf-8')
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
	    response =  server.sendmail(msg['From'], msg['To'], msg.as_string())
	return response
