#!/usr/bin/python3
"""
starts a Flask web application
"""
	
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
import secrets


def create_app():
	app = Flask(__name__)
	skey = secrets.token_urlsafe(16)
	app.secret_key = skey
	bootstrap = Bootstrap5(app)
	csrf = CSRFProtect(app)
	return app
