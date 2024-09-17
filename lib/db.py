#!/usr/bin/env python3
"""
Database functionalities
"""


import mysql.connector


def db_init():
	"""
	connect to database and extract user and admin infos,
	return user emails and admin logins.
	"""
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
	return login, mailing_list
