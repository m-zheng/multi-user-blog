from google.appengine.ext import db

from user import User
from post import Post


class Comment(db.Model):
    """post and user are the foreign keys.
    Suppose user_example is an instance of User model,
    when using "user_example.comments",
    it will return this user's all comments.

    Suppose post_example is an instance of Post model,
    when using "post_example.comments",
    it will return all comments of this post.
    """
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    post = db.ReferenceProperty(Post, collection_name="comments")
    user = db.ReferenceProperty(User, collection_name="comments")
