import os
import webapp2

import jinja2

from google.appengine.ext import db

from utility import valid_post_author, post_key, like_key
from base_handler import Handler
from models import Like


class LikeCreationHandler(Handler):
    """When a registed user upvotes the post,
    a new like entity will be created.
    Hence, the total likes will increase by one.
    If the a user upvotes the post without logging in,
    it will return to login page
    """
    def post(self, post_id):
        """This method checks whether user and post exit or not.
        If not, login page will be returned.
        If yes, before creating a new like entity,
        it checks if the user has liked the post.
        Authors can't like their own posts as well.
        """
        user = self.get_user_by_cookie()
        key = db.Key.from_path("Post", int(post_id), parent=post_key())
        post = db.get(key)

        if not user or not post:
            return self.redirect("/login?error=You have no permission.")

        if user and post and not valid_post_author(user, post):
            likes = Like.all()
            likes.filter("post = ", post)
            likes.filter("user = ", user)
            user_liked_post = likes.get()
            if not user_liked_post:
                new_like = Like(parent=like_key(),
                                post=post,
                                user=user)
                new_like.put()
                return self.redirect("/post/%s" % str(post.key().id()))
            else:
                return self.redirect("/login?error=You have upvoted it.")

        else:
            return self.redirect("/login?error=You can't upvote own post.")


class LikeDeletionHandler(Handler):
    """After a registed user upvotes a post,
    a new like entity will be created.
    Hence, the total likes will increase by one.
    If the user wants to cancel the like,
    the like entity will be deleted in datastore.
    Hence, the total likes will decrease by one as well.
    """
    def post(self, post_id):
        user = self.get_user_by_cookie()
        key = db.Key.from_path("Post", int(post_id), parent=post_key())
        post = db.get(key)

        if not user:
            self.redirect("/login")

        if user and post and not valid_post_author(user, post):
            likes = Like.all()
            likes.filter("post = ", post)
            likes.filter("user = ", user)
            user_liked_post = likes.get()
            if user_liked_post:
                user_liked_post.delete()
                return self.redirect("/post/%s" % str(post.key().id()))
            else:
                return self.redirect("/login?error=You haven't upvoted yet.")

        else:
            return self.redirect("/login?error=You can't upvote own post.")
