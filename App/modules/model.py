import datetime
from App import db


class Concept(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.utcnow(), required=True)
    title = db.StringField(max_length=255, required=True, unique=True)
    slug = db.StringField(max_length=255, required=True, unique=True)
    markup = db.StringField(required=True)
    parent = db.StringField()

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at'],
        'ordering': ['-created_at']
    }

class Stat(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.utcnow(), required=True)
    page_url = db.StringField()
    visits = db.IntField(default=0)

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at'],
        'ordering': ['-created_at']
    }

class User(db.Document):
    username = db.StringField(required=True)
    password = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow(), required=True)    
    
    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at'],
        'ordering': ['-created_at']
    }
