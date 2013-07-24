from flask.ext.wtf import Form, validators
from flask.ext.wtf.html5 import TextField


class GeolocationForm(Form):
    latitude = TextField('Latitude', [validators.Required()],
                         description=u"Insert the latitude")
    longitude = TextField('Longitude', [validators.Required()],
                          description=u"Insert the longitude")
    radius = TextField('Radius (meters)', [validators.Required()],
                       description=u"Insert the radius in meters",
                       default=500)
