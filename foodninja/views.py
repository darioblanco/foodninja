from flask import flash, redirect, request, render_template, url_for, session
from foursquare import FoursquareException

from foodninja import app, fs_client, ninja
from foodninja.forms import GeolocationForm
from foodninja.settings import FOURSQUARE


@app.route('/', methods=("GET", "POST"))
def index():
    form = GeolocationForm()
    if form.validate_on_submit():  # Only when POST
        lat = form.latitude.data
        lon = form.longitude.data
        radius = form.radius.data

        if not 'access_token' in session:
            return redirect(url_for('foursquare_auth'))

        # First chance trying to find only new places
        venues = ninja.select_lunch_place(
            session['access_token'], lat, lon,
            radius=radius, novelty='new'
        )

        if len(venues) == 0:
            # Second chance mixing old and new places
            venues = ninja.select_lunch_place(
                session['access_token'], lat, lon,
                radius=radius
            )
            if len(venues) == 0:
                # There are no more chances
                flash("The ninja can't find a place for having lunch. "
                      "Are you in the middle of the ocean or something?",
                      "error")
                return render_template("base.html", form=form,
                                       lat=lat, lon=lon)

        return render_template("base.html", form=form, lat=lat, lon=lon,
                               venues=venues[0:10], recommended_venue=venues[0])
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
    except FoursquareException:
        flash("Error connecting to Foursquare API", "error")
    else:
        session['access_token'] = access_token

    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/policy')
def policy():
    return render_template('policy.html')
