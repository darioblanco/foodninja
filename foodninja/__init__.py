"""Webapp package initializing the global app object"""
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from foursquare import Foursquare

from foodninja.settings import BASEURL, DEBUG, FOURSQUARE, SECRET_KEY

app = Flask(__name__)
app.config.update({
    'DEBUG': DEBUG,
    'SECRET_KEY': SECRET_KEY
})

app.config['DEBUG_TB_PROFILER_ENABLED'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

# Foursquare client
fs_client = Foursquare(client_id=FOURSQUARE['CLIENT_ID'],
                       client_secret=FOURSQUARE['CLIENT_SECRET'],
                       redirect_uri=BASEURL + FOURSQUARE['REDIRECT_URI'])

import views
