from flask import flash, request, render_template

from foodninja import app
from foodninja.forms import GeolocationForm
from foodninja.foursquare import Foursquare, FoursquareAuth
from foodninja.settings import FOURSQUARE


@app.route('/', methods=("GET", "POST"))
def index():
    form = GeolocationForm()
    if form.validate_on_submit():
        lat = form.latitude.data
        lon = form.longitude.data
        radius = form.radius.data

        auth = FoursquareAuth(FOURSQUARE['CLIENT_ID'],
                              FOURSQUARE['CLIENT_SECRET'])
        foursq = Foursquare(auth)
        cid = request.form.get('cid', FOURSQUARE['CATEGORY_ID'])
        latlon = '{0},{1}'.format(lat, lon)  # XX.XX,YY.YY
        try:
            res = foursq.request('venues', aspect='search', ll=latlon,
                                 radius=radius, categoryId=cid)
            venues = res['response']['venues']
        except Exception:
            venues = None
            flash("Unable to connect to Foursquare", "error")
        else:
            flash("Success")

        return render_template("base.html", form=form, venues=venues,
                               lat=lat, lon=lon)
    return render_template('base.html', form=form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/imprint')
def imprint():
    return render_template('imprint.html')
