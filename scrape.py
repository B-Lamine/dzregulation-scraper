#!/usr/bin/env python3
"""
scraper main entry point
"""


from lib.scraper import get_link, download_file
from lib.db import db_init
from lib.mail import send_email


if __name__ == '__main__':
	url = "http://www.miph.gov.dz/fr/telechargements/"
	file_url = get_link(url)
	download_file(file_url)
	login, mailing_list = db_init()
	for recipient in mailing_list:
		subject = "Update alert"
		body = 'Dear user; Please find attached the latest file updates.'
		send_email(recipient, login, subject, body)
