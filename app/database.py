#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask_sqlalchemy import SQLAlchemy
import pymysql
from sqlalchemy.sql import text
from sqlalchemy import insert


username = 'portfoo'
password = 'portfoo_pwd'
userpass = 'mysql+pymysql://' + username + ':' + password + '@'
server   = '127.0.0.1'
dbname   = '/portfoo_db'
socket   = '?unix_socket=/var/run/mysqld/mysqld.sock'


def init_db(app):
	app.config['SQLALCHEMY_DATABASE_URI'] = userpass + server + dbname + socket
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
	db = SQLAlchemy()
	db.init_app(app)

	class MailingList(db.Model):
		__tablename__ = "mailing_list"
		id = db.Column(db.Integer, primary_key=True)
		name = db.Column(db.String)
		email = db.Column(db.String)
		
		def __init__(self, **kwargs):
			self.name = kwargs.get('name', 'None')
			self.email = kwargs.get('email', 'None')
	return db, MailingList
