foodninja
==========

Where to have lunch? Listen to the ninja!

This project is a fork of [valetar/lunchlotto](https://github.com/valetar/lunchlotto).


### Workaround for the `SSL3 certificate verify failed`
In order to get a proper access token for the specified client credentials in a local set up, we have to do some extra work for avoiding the following error:

> [Errno 1] _ssl.c:504: error:14090086:SSL routines:SSL3_GET_SERVER_CERTIFICATE:certificate verify failed

As stated [here](http://stackoverflow.com/questions/13321302/python-foursquare-ssl3-certificate-verify-failed), there is a way for fixing this problem and test your Foursquare APP locally:

1. Go to your python httplib2 dir. For instance, in a `virtualenv`: `$VIRTUAL_ENV/lib/pythonX.X/site-packages/httplib2`

2. Download http://curl.haxx.se/ca/cacert.pem

> wget http://curl.haxx.se/ca/cacert.pem

3. Backup the existing certificate as `backup_cacerts.txt`

3. Store `cacert.pem` as `cacerts.txt` in that folder.
> mv cacert.pem cacerts.txt
