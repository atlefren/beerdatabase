# -*- coding: utf-8 -*-
import os

from flask import Flask
from webassets.loaders import PythonLoader
from flask.ext.assets import Environment
# from flask_googlelogin import GoogleLogin
# from flask_login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.jsontools import DynamicJSONEncoder

app = Flask(__name__)

app.json_encoder = DynamicJSONEncoder

# load config
app.config.update(
    DEBUG=os.environ.get('DEBUG', False),
    SECRET_KEY=os.environ.get('SECRET_KEY', ''),
    # GOOGLE_LOGIN_CLIENT_ID=os.environ.get('GOOGLE_LOGIN_CLIENT_ID', ''),
    # GOOGLE_LOGIN_CLIENT_SECRET=os.environ.get('GOOGLE_LOGIN_CLIENT_SECRET', ''),
    # GOOGLE_LOGIN_REDIRECT_URI=os.environ.get('GOOGLE_LOGIN_REDIRECT_URI', ''),
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI', 'postgres://beer:beer@localhost/beer'),
)

db = SQLAlchemy(app)

# setup assetbundle

assets = Environment(app)
assets.debug = False # app.debug # (debug=True fucks up jsx)

bundles = PythonLoader('web.assetbundles').load_bundles()
for name, bundle in bundles.iteritems():
    assets.register(name, bundle)

# add various views
from web import views
from web import api

app.db_session = db.session
