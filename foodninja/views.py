from flask import request, render_template

from foodninja import app
from foodninja.foursquare import Foursquare, FoursquareAuth
from foodninja.settings import FOURSQUARE


@app.route('/', methods=['POST', 'GET'])
def index():
    auth = FoursquareAuth(FOURSQUARE['CLIENT_ID'], FOURSQUARE['CLIENT_SECRET'])
    foursq = Foursquare(auth)
    venues = None
    error = None
    lat = ''
    lon = ''
    if request.method == 'POST':
        lat = request.form.get('lat', '')
        lon = request.form.get('lon', '')
        radius = request.form.get('radius', 500)
        cid = request.form.get('cid', FOURSQUARE['CATEGORY_ID'])
        latlon = '{0}.{1},{2}.{3}'.format(lat.split('.')[0],
                                          lat.split('.')[1],
                                          lon.split('.')[0],
                                          lon.split('.')[1])
        try:
            res = foursq.request('venues', aspect='search', ll=latlon,
                                 radius=radius, categoryId=cid)
            venues = res['response']['venues']
        except Exception as e:
            error = 'Connection error - %s ' % e
    title = 'Where can I go for lunch today?'
    sitename = 'lunchlotto'
    return render_template('base.html', venues=venues, error=error,
                           lat=lat, lon=lon, title=title, sitename=sitename)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/imprint')
def imprint():
    return render_template('imprint.html')
