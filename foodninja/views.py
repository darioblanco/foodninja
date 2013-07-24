from flask import flash, redirect, request, render_template, url_for
from foursquare import FoursquareException

from foodninja import app, fs_client, ninja
from foodninja.forms import GeolocationForm
from foodninja.settings import FOURSQUARE


@app.route('/', methods=("GET", "POST"))
def index():
    form = GeolocationForm()
    if form.validate_on_submit():
        lat = form.latitude.data
        lon = form.longitude.data
        radius = form.radius.data

        place, venues = ninja.select_lunch_place(lat, lon, radius)

        return render_template("base.html", form=form, place=place,
                               venues=venues, lat=lat, lon=lon)
    return render_template('base.html', form=form)


@app.route('/auth')
def foursquare_auth():
    """Builds the authorization url for the application"""
    auth_uri = fs_client.oauth.auth_url()
    return redirect(auth_uri)


@app.route(FOURSQUARE['REDIRECT_URI'])
def foursquare_redirect():
    """Gets the user's access token from Foursquare"""
    code = request.args.get('code', '')

    try:
        # Interrogate foursquare's servers to get the user's access_token
        access_token = fs_client.oauth.get_token(code)
        # Apply the returned access token to the client
        fs_client.set_access_token(access_token)
    except FoursquareException:
        flash("Error connecting to Foursquare API", "error")

    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/imprint')
def imprint():
    return render_template('imprint.html')
