import os

DEBUG = True
SECRET_KEY = "d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f"
BASEURL = 'http://localhost:5000'

BASEDIR = os.path.abspath(os.path.dirname(__file__).replace('\\', '/'))

# Testing credentials
FOURSQUARE = {
    'CLIENT_ID': u'NQPFYL4UQQDWXPMXVRJNR5MNC3EZIO2FEEJYTVCJB1G35JNS',
    'CLIENT_SECRET': u'2KWDC3Z04Z0H33PJRGKLTUOY43CLNTRDPATZHF1UL3HQ35QE',
    'REDIRECT_URI': '/redirect'
}
