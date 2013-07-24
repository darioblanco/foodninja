from flask import flash, redirect, request, render_template, url_for
from foursquare import FoursquareException, InvalidAuth

from foodninja import app, fs_client
from foodninja.forms import GeolocationForm
from foodninja.settings import FOURSQUARE


@app.route('/', methods=("GET", "POST"))
def index():
    form = GeolocationForm()
    if form.validate_on_submit():
        lat = form.latitude.data
        lon = form.longitude.data
        radius = form.radius.data

        params = {'ll': '{0},{1}'.format(lat, lon)}  # XX.XX,YY.YY}
        if radius:
            params['radius'] = radius
        try:
            # Get the user's data
            explore_resp = fs_client.venues.explore(params=params)
        except InvalidAuth:
            return redirect(url_for('foursquare_auth'))
        except FoursquareException:
            flash("Unable to connect to Foursquare", "error")
        else:
            items, venues = [], []
            for group in explore_resp['groups']:
                if group['name'] == 'recommended':
                    items = group['items']

            if len(items) == 0:
                flash("The ninja can't find a place for having lunch. "
                      "Are you in the middle of the ocean or something?",
                      "error")
            else:
                for item in group['items']:
                    venues.append(item['venue'])

            if 'warning' in explore_resp:
                flash(explore_resp['warning']['text'], "warning")
            if 'suggestedRadius' in explore_resp:
                flash("We recomend you to use a radius of "
                      "{0} meters".format(explore_resp['suggestedRadius']),
                      "info")
            return render_template("base.html", form=form, venues=venues,
                                   lat=lat, lon=lon)
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
    except FoursquareException as e:
        flash("Error connecting to Foursquare API", "error")

    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/imprint')
def imprint():
    return render_template('imprint.html')
