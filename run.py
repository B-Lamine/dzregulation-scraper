#!/usr/bin/python3
"""
Web app main entry point.
"""

from app import create_app
from app.database import init_db
from flask import Flask, render_template, request, send_file, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email
import os


# instantiate a Flask app
app = create_app()
# instantiate database and connect app to table of users data
db, MailingList = init_db(app)


class SubsForm(FlaskForm):
	"""
	Form fields class to register user data.
	"""
	name = StringField('Full name :', validators=[DataRequired()])
	email = EmailField('Email address', validators=[DataRequired(), Email()])
	submit = SubmitField('Submit')


@app.route('/', strict_slashes=False)
@app.route('/about', strict_slashes=False)
def index():
	"""
	index/about page
	"""
	return render_template('jumbo.html')


@app.route('/subscribe', strict_slashes=False, methods=['GET', 'POST'])
def subscribe():
	"""
	Subscription page that also handles storing data to database.
	Files are also listed via this page.
	"""
	form = SubsForm()
	# get files available for download
	files_list = os.popen('ls app/storage').read()[:-1].split("\n")
	message = ""
	if request.method == 'POST':
		if form.validate_on_submit():
			new_sub = MailingList(name=request.form['name'], email=request.form['email'])
			db.session.add(new_sub)
			db.session.commit()
			return redirect(url_for('subscribe'))
		else:
			message = "something is wrong."
			return render_template('test.html', files=files_list, form=form, message=message)
	else:
		emails = db.session.execute(db.select(MailingList)).scalars()
		return render_template('test.html', files=files_list, form=form, message=message)


@app.route('/download/<string:filename>', strict_slashes=False)
def download(filename):
	"""
	download files from storage
	"""
	filepath = "storage/" + filename
	return send_file(filepath, as_attachment=True)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port='5000')
