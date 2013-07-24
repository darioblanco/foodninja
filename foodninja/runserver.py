#!/usr/bin/env python

from foodninja import app
from foodninja.settings import DEBUG

if __name__ == '__main__':
    app.run(debug=DEBUG)
