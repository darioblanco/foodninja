from flask.ext.wtf import Form
from flask.ext.wtf.html5 import TextField, IntegerField
from wtforms.validators import Optional, Required, ValidationError


def coordinate_length(min=-1, max=-1):

    def _length(form, field):
        try:
            l = float(field.data)
        except ValueError:
            raise ValidationError('Invalid coordinate number')

        if l < min or max != -1 and l > max:
            raise ValidationError(
                'Coordinate must be between {0} and {1}.'.format(min, max))

    return _length


class GeolocationForm(Form):
    latitude = TextField(
        'Latitude', [Required(), coordinate_length(min=-90, max=90)],
        description=u"Insert the latitude"
    )
    longitude = TextField(
        'Longitude', [Required(), coordinate_length(min=-180, max=180)],
        description=u"Insert the longitude"
    )
    radius = IntegerField('Radius (meters)', [Optional()],
                          description=u"Insert the radius in meters",
                          default=500)
