#!/usr/bin/python3
"""
starts a Flask web application
"""

import pymysql
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm#, CSRFProtect
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email
import secrets
from sqlalchemy import insert

db = SQLAlchemy()
app = Flask(__name__)

skey = secrets.token_urlsafe(16)
app.secret_key = skey
# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
#csrf = CSRFProtect(app)

username = 'portfoo'
password = 'portfoo_pwd'
userpass = 'mysql+pymysql://' + username + ':' + password + '@'
server   = '127.0.0.1'
dbname   = '/portfoo_db'
socket   = '?unix_socket=/var/run/mysqld/mysqld.sock'

app.config['SQLALCHEMY_DATABASE_URI'] = userpass + server + dbname + socket
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

class SubsForm(FlaskForm):
    name = StringField('Full name :', validators=[DataRequired()])
    email = EmailField('Email address', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

class MailingList(db.Model):
    __tablename__ = "mailing_list"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'None')
        self.email = kwargs.get('email', 'None')

@app.route('/', strict_slashes=False, methods=['GET', 'POST'])
def index():
    form = SubsForm()
    message = ""
    if request.method == 'POST':
        if form.validate_on_submit():
            new_sub = MailingList(name=request.form['name'], email=request.form['email'])
            db.session.add(new_sub)
            db.session.commit()
        else:
            message = "something is wrong."
        emails = db.session.execute(db.select(MailingList)).scalars()
        return render_template('index.html', emails=emails, form=form, message=message)# dbtext
    else:
        emails = db.session.execute(db.select(MailingList)).scalars()
        return render_template('index.html', emails=emails, form=form, message=message)# dbtext
#    try:
#        emails = db.session.execute(db.select(MailingList)).scalars()
#            #.filter_by(style='knee-high')
#            #.order_by(Sock.name)).scalars()
#
##        dbtext = '<ul>'
##        for mail in emails:
##            dbtext += '<li>' + mail.name + ':: ' + mail.email + '</li>'
##        dbtext += '</ul>'
#        return render_template('index.html', emails=emails, form=form, message=message)# dbtext
#    except Exception as e:
#        # e holds description of the error
#        error_text = "<p>The error:<br>" + str(e) + "</p>"
#        hed = '<h1>Something is broken.</h1>'
#        return hed + error_text

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
