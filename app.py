#!/usr/bin/python3
"""
starts a Flask web application
"""

from assets import create_app
from assets.database import init_db
from flask import Flask, render_template, request, send_file, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
# from flask_modals import Modal, render_template_modal
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email
import os


app = create_app()
db, MailingList = init_db(app)
# modal = Modal(app)


class SubsForm(FlaskForm):
    name = StringField('Full name :', validators=[DataRequired()])
    email = EmailField('Email address', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')


@app.route('/', strict_slashes=False)
@app.route('/about', strict_slashes=False)
def index():
        return render_template('jumbo.html')

@app.route('/subscribe', strict_slashes=False, methods=['GET', 'POST'])
def subscribe():
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

@app.route('/consult', strict_slashes=False)
def consult():
    files_list = os.popen('ls storage').read()[:-1].split("\n")
    return render_template('consult.html', files=files_list)

@app.route('/download/<string:filename>', strict_slashes=False)
def download(filename):
    filepath = "storage/" + filename
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
