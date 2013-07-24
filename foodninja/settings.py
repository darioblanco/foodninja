import os

DEBUG = True
SECRET_KEY = "secret"
BASEURL = 'http://localhost:5000'

BASEDIR = os.path.abspath(os.path.dirname(__file__).replace('\\', '/'))

FOURSQUARE = {
    'CLIENT_ID': u'NQPFYL4UQQDWXPMXVRJNR5MNC3EZIO2FEEJYTVCJB1G35JNS',
    'CLIENT_SECRET': u'2KWDC3Z04Z0H33PJRGKLTUOY43CLNTRDPATZHF1UL3HQ35QE',
    'REDIRECT_URI': '/redirect'
}
