"""Webapp package initializing the global app object"""
from flask import Flask

from foodninja.settings import DEBUG, SECRET_KEY

app = Flask(__name__)
app.config.update({
    'DEBUG': DEBUG,
    'SECRET_KEY': SECRET_KEY
})

import views
