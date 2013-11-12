import hashlib
from functools import wraps
from flask import request, Response
from model import User


def check_auth(username, password):
    user = User.objects.get_or_404(username=username)
    return hashlib.sha1(password).hexdigest() == user.password


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
