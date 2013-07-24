"""Webapp package initializing the global app object"""
from flask import Flask

app = Flask(__name__)

import views
