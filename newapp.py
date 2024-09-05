#!/usr/bin/python3
"""
starts a Flask web application
"""

# import pymysql
from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.sql import text
############################################
from flask import Flask,render_template, request
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'portfoo'
app.config['MYSQL_PASSWORD'] = 'portfoo_db'
app.config['MYSQL_DB'] = 'portfoo_db'
 
mysql = MySQL(app)
 
 
# @app.route('/', strict_slashes=False, methods = ['POST', 'GET'])
# def index():
#     #if request.method == 'GET':
#     #    return "Login via the login Form"
#      
#     #if request.method == 'POST':
#     name = request.form['name']
#     age = request.form['age']
#     cursor = mysql.connection.cursor()
#     cursor.execute(''' INSERT INTO info_table VALUES(%s,%s)''',(name,age))
#     mysql.connection.commit()
#     cursor.close()
#     return f"Done!!"
#########################################

@app.route('/', strict_slashes=False)
def index():
    try:
        cursor = mysql.connection.cursor()
        #cursor.execute(''' INSERT INTO info_table VALUES(%s,%s)''',(name,age))
        cursor.execute("SELECT name, email FROM mailing_list")
        data = [list(el) for el in cursor.fetchall()]
        emails = [el[1] for el in data]
        #mysql.connection.commit()
        cursor.close()

        dbtext = '<ul>'
        for mail in emails:
            dbtext += '<li>' + mail.name + ':: ' + mail.email + '</li>'
        dbtext += '</ul>'
        return dbtext
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
