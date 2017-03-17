from google.appengine.ext import db


class User(db.Model):
    """This is User model and its attributes in the datastore"""
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.EmailProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
