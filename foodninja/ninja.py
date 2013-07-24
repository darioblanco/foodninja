from heapq import heappush, heappop

from flask import flash
from foursquare import Foursquare, FoursquareException

from foodninja.settings import BLACKLISTED_CATEGORIES


def select_lunch_place(access_token, latitude, longitude,
                       radius=None, novelty=None):
    """Selects a venue from all of the given by foursquare,
    based on a priority algorithm
    """
    params = {
        'll': '{0},{1}'.format(latitude, longitude),
        'section': 'food',
        'venuePhotos': 1
    }
    if radius:
        params['radius'] = radius
    if novelty:
        params['novelty'] = novelty

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
            return []

        venues_heap = []
        for item in group['items']:
            if (item['venue']['categories'][0]['name']
                    not in BLACKLISTED_CATEGORIES):
                heappush(venues_heap,
                         (_calculate_priority(item['venue']), item['venue']))

        if 'suggestedRadius' in response:
            flash("We recomend you to use a radius of "
                  "{0} meters".format(response['suggestedRadius']),
                  "info")

        return heapsort(venues_heap)


def _calculate_priority(venue):
    """Returns the priority of the given venue based on some of its parameters"""
    priority = 0

    # Punish if the ranking is lower
    if 'rating' in venue:
        priority += 10 - venue['rating']
    else:
        # When there is no ranking, 4 is the default punishment
        priority += 4

    # Punish each 15m of distance
    priority += venue['location']['distance'] / 15

    # Punish if you don't like it
    if not venue['like']:
        priority += 1

    # Punish if there are no likes
    if venue['likes']['count'] == 0:
        priority += 1

    # Punish if there are no specials
    if venue['specials']['count'] == 0:
        priority += 1

    # Punish if there are no photos
    if venue['photos']['count'] == 0:
        priority += 1

    # Punish if there are no people checked in
    if venue['hereNow']['count'] == 0:
        priority += 1

    return priority


def heapsort(iterable):
    """Orders the heap by priority (less value = higher priority)"""
    h = []
    for value in iterable:
        heappush(h, value)
    return [heappop(h)[1] for i in range(len(h))]
