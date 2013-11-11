import hashlib
from functools import wraps
from flask import request, Response


def check_auth(username, password):
    return hashlib.sha1(username).hexdigest() == 'd25b8582a731d5187d9820d49ca05a8593bf058e' and hashlib.sha1(password).hexdigest() == '9cdb83764d9cd85af163bb54c7add2674a97f327'


def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
