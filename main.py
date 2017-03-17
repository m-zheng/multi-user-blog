import hashlib
import os
import re
import random
import string
import webapp2

import jinja2

from google.appengine.ext import db

from handlers import (Handler,
                      RegisterHandler,
                      LoginHandler,
                      DashboardHandler,
                      LogoutHandler,
                      ResetPasswordHandler,
                      RefreshHandler,
                      PostCreationHandler,
                      PostIndexHandler,
                      PostShowHandler,
                      PostEditHandler,
                      PostDeletionHandler,
                      CommentEditHandler,
                      CommentDeletionHandler,
                      LikeCreationHandler,
                      LikeDeletionHandler,
                      valid_val_hash,
                      SALT,
                      user_key,
                      valid_username,
                      valid_password_format,
                      valid_email,
                      register,)

from models import Post, User, Comment, Like


app = webapp2.WSGIApplication([
    ("/register", RegisterHandler),
    ("/login", LoginHandler),
    ("/logout", LogoutHandler),
    ("/dashboard", DashboardHandler),
    ("/reset", ResetPasswordHandler),
    ("/refresh", RefreshHandler),
    ("/", PostIndexHandler),
    ("/post/?", PostIndexHandler),
    ("/post/create", PostCreationHandler),
    ("/post/([0-9]+)", PostShowHandler),
    ("/post/([0-9]+)/edit", PostEditHandler),
    ("/post/([0-9]+)/delete", PostDeletionHandler),
    ("/post/([0-9]+)/upvote", LikeCreationHandler),
    ("/post/([0-9]+)/downvote", LikeDeletionHandler),
    ("/comment/([0-9]+)/edit", CommentEditHandler),
    ("/comment/([0-9]+)/delete", CommentDeletionHandler),
    ], debug=True)
