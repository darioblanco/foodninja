import os

DEBUG = True
SECRET_KEY = "secret"
BASEURL = 'http://localhost:5000'

BASEDIR = os.path.abspath(os.path.dirname(__file__).replace('\\', '/'))

FOURSQUARE = {
    'CLIENT_ID': u'',
    'CLIENT_SECRET': u'',
    'REDIRECT_URI': '/redirect'
}
