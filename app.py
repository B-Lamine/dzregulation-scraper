#!/usr/bin/python3
"""
starts a Flask web application
"""

import pymysql
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

db = SQLAlchemy()
app = Flask(__name__)

username = 'portfoo'
password = 'portfoo_pwd'
userpass = 'mysql+pymysql://' + username + ':' + password + '@'
server   = '127.0.0.1'
dbname   = '/portfoo_db'
socket   = '?unix_socket=/var/run/mysqld/mysqld.sock'

app.config['SQLALCHEMY_DATABASE_URI'] = userpass + server + dbname + socket
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

class MailingList(db.Model):
    __tablename__ = "mailing_list"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)

@app.route('/', strict_slashes=False)
def index():
    try:
        emails = db.session.execute(db.select(MailingList)).scalars()
            #.filter_by(style='knee-high')
            #.order_by(Sock.name)).scalars()

#        dbtext = '<ul>'
#        for mail in emails:
#            dbtext += '<li>' + mail.name + ':: ' + mail.email + '</li>'
#        dbtext += '</ul>'
        return render_template('index.html', emails=emails)# dbtext
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

# @app.route('/', strict_slashes=False)
# def testdb():
#     try:
#         db.session.query(text('1')).from_statement(text('SELECT 1')).all()
#         return '<h1>It works.</h1>'
#     except Exception as e:
#         # e holds description of the error
#         error_text = "<p>The error:<br>" + str(e) + "</p>"
#         hed = '<h1>Something is broken.</h1>'
#         return hed + error_text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
