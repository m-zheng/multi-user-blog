from google.appengine.ext import db

from user import User
from post import Post


class Like(db.Model):
    """This is Like model in datatore.
    There are two foreign keys in this model.
    One is post and the other is user.
    They refer to Post and User model respectively.
    Suppose user_example is an instance of User model,
    post_example is an instance of Post model.
    Using "user_example.likes" will fetch all user_example's liked posts.
    Using "post_example.users" will fetch a list of people who liked this post.
    """
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    post = db.ReferenceProperty(Post, collection_name="likes")
    user = db.ReferenceProperty(User, collection_name="likes")
