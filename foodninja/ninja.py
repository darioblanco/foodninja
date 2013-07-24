import random

from flask import flash
from foursquare import Foursquare, FoursquareException

from foodninja.settings import BLACKLISTED_CATEGORIES


def select_lunch_place(access_token, latitude, longitude,
                       radius=None, novelty='new'):
    params = {
        'll': '{0},{1}'.format(latitude, longitude),
        'section': 'food',
        'novelty': novelty
    }
    if radius:
        params['radius'] = radius

    client = Foursquare(access_token=access_token)

    try:
        response = client.venues.explore(params=params)
    except FoursquareException:
        flash("Unable to connect to Foursquare", "error")
    else:
        items = []
        for group in response['groups']:
            if group['name'] == 'recommended':
                items = group['items']

        if len(items) == 0:
            flash("The ninja can't find a place for having lunch. "
                  "Are you in the middle of the ocean or something?",
                  "error")
            return False, False

        venues = []
        for item in group['items']:
            if item['venue']['categories'][0]['name'] not in BLACKLISTED_CATEGORIES:
                venues.append(item['venue'])

        if 'warning' in response:
            flash(response['warning']['text'], "warning")

        if 'suggestedRadius' in response:
            flash("We recomend you to use a radius of "
                  "{0} meters".format(response['suggestedRadius']),
                  "info")

        return random.choice(venues), venues
