from datetime import datetime
from functools import wraps
from flask import request
from model import Stat

def track_stats(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        page_stat = Stat.objects(page_url=request.base_url).first()
        if not page_stat:
            page_stat = Stat()
            page_stat.page_url = request.base_url
        page_stat.created_at = datetime.utcnow()
        page_stat.visits += 1
        page_stat.save()
        return f(*args, **kwargs)
    return decorated
