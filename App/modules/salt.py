import hashlib
from functools import wraps
from flask import request, Response, jsonify
from App import app


def check_salt():
    user = request.form.get('user')
    score = request.form.get('score')
    if not score:
        score = "0"
    salt = request.form.get('salt')
    salt_str = user + score + app.config['SALT_PHRASE']
    local_salt = hashlib.sha256(salt_str.encode('utf-8')).hexdigest()
    print(local_salt)
    return salt == local_salt


def requires_salt(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not check_salt():
            return jsonify(ok=False,reason='failed salt check')
        return f(*args, **kwargs)
    return decorated
