#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask_sqlalchemy import SQLAlchemy
import pymysql
from sqlalchemy import insert
from sqlalchemy.sql import text


# database infos
username = 'portfoo'
password = 'portfoo_pwd'
userpass = 'mysql+pymysql://' + username + ':' + password + '@'
server   = '127.0.0.1'
dbname   = '/portfoo_db'
socket   = '?unix_socket=/var/run/mysqld/mysqld.sock'


def init_db(app):
	"""
	initialize database and connect app to it
	"""
	app.config['SQLALCHEMY_DATABASE_URI'] = userpass + server + dbname + socket
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
	db = SQLAlchemy()
	db.init_app(app)

	class MailingList(db.Model):
		"""
		user data table
		"""
		__tablename__ = "mailing_list"
		id = db.Column(db.Integer, primary_key=True)
		name = db.Column(db.String)
		email = db.Column(db.String)
		
		def __init__(self, **kwargs):
			"""
			initialize a new entry in the MailingList table
			"""
			self.name = kwargs.get('name', 'None')
			self.email = kwargs.get('email', 'None')
	return db, MailingList
