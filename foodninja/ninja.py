import random

from flask import flash
from foursquare import FoursquareException, InvalidAuth

from foodninja import fs_client


def select_lunch_place(latitude, longitude, radius=None, novelty='new'):
    params = {
        'll': '{0},{1}'.format(latitude, longitude),
        'section': 'food',
        'novelty': novelty
    }
    if radius:
        params['radius'] = radius

    try:
        response = fs_client.venues.explore(params=params)
    except InvalidAuth:
        raise
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

        venues = [item['venue'] for item in group['items']]

        if 'warning' in response:
            flash(response['warning']['text'], "warning")

        if 'suggestedRadius' in response:
            flash("We recomend you to use a radius of "
                  "{0} meters".format(response['suggestedRadius']),
                  "info")

        return random.choice(venues), venues
