#!/usr/bin/env python
import argparse

from foodninja import app
from foodninja.settings import DEBUG


if __name__ == '__main__':
    """Runs the foodninja application"""
    parser = argparse.ArgumentParser(description='Run the foodninja webserver')
    parser.add_argument("--host", type=str, default='localhost',
                        help="Webserver host")
    parser.add_argument("--port", type=int, default=5000,
                        help="Webserver port")
    parser.add_argument("--debug", action="store_true", default=DEBUG,
                        help="Set debug mode")
    args_dict = vars(parser.parse_args())
    app.run(host=args_dict['host'], port=args_dict['port'],
            debug=args_dict['debug'])
