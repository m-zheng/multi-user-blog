import hashlib
import re
import random
import string

from google.appengine.ext import db

from models import Post, User, Comment, Like


def valid_username(username):
    """This function checks whether the username is valid or not."""
    match = re.search(r'^[a-zA-Z0-9_-]{3,20}$', username)
    if match:
        return match.group()


def valid_password_format(password):
    """ This function checks whether the password format is valid or not."""
    match = re.search(r'^.{3,20}$', password)
    if match:
        return match.group()


def valid_email(email):
    """This function checks whether the email is valid or not."""
    match = re.search(r'^[\S]+@[\S]+.[\S]+$', email)
    if match:
        return match.group()


SALT = "THIS IS A TEST SALT"


def make_val_hash(val, SALT):
    """This function encrypts the value with salt.
    It returns the digest of the strings.
    """
    val = str(val)
    val_hash = hashlib.sha256(val + SALT).hexdigest()
    return "%s|%s" % (val, val_hash)


def valid_val_hash(encrypted_string, SALT):
    """This function checks whether the encrypted value is correct or not."""
    val = encrypted_string.split("|")[0]
    if encrypted_string == make_val_hash(val, SALT):
        return True


def make_salt():
    """This function rendomly generates 5 strings"""
    return "".join(random.choice(string.letters) for x in xrange(5))


def make_pw_hash(name, pw, salt=None):
    """This function encrypts the password with salt.
    The salt is randomly generated if it's not given in the arguments.
    It returns the digest of the strings.
    """
    if not salt:
        salt = make_salt()
    encrypted_string = hashlib.sha256(name + pw + salt).hexdigest()
    return "%s,%s" % (encrypted_string, salt)


def valid_pw(name, pw, pw_hash):
    """This function checks if the encrypted password is correct"""
    pw_salt = pw_hash.split(",")[1]
    if pw_hash == make_pw_hash(name, pw, pw_salt):
        return True


def check_existing_user(username):
    """This function checks if the username is already in database."""
    username = str(username)
    users = User.all().filter("username = ", username).get()
    if users:
        return True


def valid_post_author(user, post):
    """This function checks whether the post was created by the user"""
    if str(user.key().id()) == str(post.user.key().id()):
        return True


def register(username, password, email=None):
    """This function creates a new entity in the datastore.
    It returns a key of this entity
    """
    password = make_pw_hash(username, password)
    new_user = User(parent=user_key(),
                    username=username,
                    password=password,
                    email=email)
    username_key = new_user.put()
    return username_key


def post_key(name="default"):
    """It builds a new Key object from posts."""
    return db.Key.from_path("posts", name)


def comment_key(name="default"):
    """It builds a new Key object from comments."""
    return db.Key.from_path("comments", name)


def like_key(name="default"):
    """It builds a new Key object from likes."""
    return db.Key.from_path("likes", name)


def user_key(name='default'):
    """It builds a new Key object from users."""
    return db.Key.from_path('users', name)
