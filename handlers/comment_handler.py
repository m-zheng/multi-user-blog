import os
import webapp2

import jinja2

from google.appengine.ext import db

from base_handler import Handler
from utility import comment_key


class CommentEditHandler(Handler):
    """Post method will update the comment,
    when the user is logged in,
    the comment exits and the new comment is not blank.
    """
    def post(self, comment_id):
        """Comment creation method can be found
        in PostShowHandler module, PostShowHandler class.
        When updating a comment, it won't change the author.
        """
        user = self.get_user_by_cookie()
        key = db.Key.from_path("Comment",
                               int(comment_id),
                               parent=comment_key())
        comment = db.get(key)
        input_comment_cotent = self.request.get("comment_content")

        if user and \
           comment and \
           input_comment_cotent and \
           user.username == comment.user.username:
            comment.content = input_comment_cotent
            comment.put()

        self.redirect("/post/%s" % str(comment.post.key().id()))


class CommentDeletionHandler(Handler):
    """Post method will delete the comment,
    when the user is logged in and the comment exists.
    """
    def post(self, comment_id):
        user = self.get_user_by_cookie()
        key = db.Key.from_path("Comment",
                               int(comment_id),
                               parent=comment_key())
        comment = db.get(key)
        if user and comment and user.username == comment.user.username:
            comment.delete()
        self.redirect("/post/%s" % str(comment.post.key().id()))
