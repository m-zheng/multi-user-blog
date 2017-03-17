import os
import webapp2

import jinja2

from google.appengine.ext import db

from utility import valid_post_author, post_key, comment_key
from base_handler import Handler
from models import Post, Comment


class PostCreationHandler(Handler):
    """Only registed user can create a new post."""
    def get(self, subject="", content="", error=""):
        user = self.get_user_by_cookie()
        if user:
            self.render("Post/create.html",
                        subject=subject,
                        content=content,
                        error=error,
                        user=user)
        else:
            return self.redirect("/login?error=Sorry, you have no permission.")

    def post(self):
        user = self.get_user_by_cookie()
        if user:
            subject = self.request.get("subject")
            content = self.request.get("content")
            # Using "<br>" to replace "\n" will display the newline in html.
            # But this will make some harmful tags affect html,
            # such as <script>alert("hack me")</script>.
            content = content.replace("\n", "<br>")
            if subject and content:
                new_post = Post(parent=post_key(),
                                subject=subject,
                                content=content,
                                user=user)
                new_post.put()
                self.redirect("/post/%s" % str(new_post.key().id()))
            else:
                error = "Please input subject and content for a post."
                self.render("Post/create.html",
                            subject=subject,
                            content=content,
                            error=error)
        else:
            return self.redirect("/login?error=Sorry, you have no permission.")


class PostIndexHandler(Handler):
    """It will display all posts"""
    def get(self):
        # Descending sort order
        # is denoted by a hyphen (-) preceding the property name
        posts = Post.all().order("-created")
        user = self.get_user_by_cookie()
        self.render("Post/index.html", posts=posts, user=user)


class PostShowHandler(Handler):
    def get(self, post_id):
        """This get method displays individual post"""
        user = self.get_user_by_cookie()
        key = db.Key.from_path("Post", int(post_id), parent=post_key())
        post = db.get(key)
        if not post:
            self.error(404)
            return
        self.render("Post/show.html", post=post, user=user)

    def post(self, post_id):
        """This post method will create a new comment"""
        user = self.get_user_by_cookie()
        # db.Key.from_path is looking for an object of type Post,
        # with an id of post_id,
        # and a parent equal to the return value of the post_key() method.
        key = db.Key.from_path("Post", int(post_id), parent=post_key())
        post = db.get(key)
        if user and post:
            input_comment_content = self.request.get("comment")
            if input_comment_content:
                new_comment = Comment(parent=comment_key(),
                                      content=input_comment_content,
                                      post=post,
                                      user=user)
                new_comment.put()
                self.redirect("/post/%s" % str(post.key().id()))
            else:
                error = "Please input a comment for a post."
                self.render("Post/show.html",
                            post=post,
                            user=user,
                            error=error)
        else:
            return self.redirect("/login?error=Sorry, you have no permission.")


class PostEditHandler(Handler):
    def get(self, post_id):
        """If an anonymous user edits a post,
        the login page will be returned.
        If the user is not the post author,
        the login page and permission error message will be returned.
        """
        user = self.get_user_by_cookie()
        key = db.Key.from_path("Post", int(post_id), parent=post_key())
        post = db.get(key)

        if not user:
            self.redirect("/login")

        if user and post and valid_post_author(user, post):
            self.render("Post/edit.html", user=user, post=post)
        else:
            return self.redirect("/login?error=Sorry, you have no permission.")

    def post(self, post_id):
        """when a post author updates the post,
        it will check whether the post subject and content are blank or not.
        """
        user = self.get_user_by_cookie()
        key = db.Key.from_path("Post", int(post_id), parent=post_key())
        post = db.get(key)
        if user and post and valid_post_author(user, post):
            subject = self.request.get("subject")
            content = self.request.get("content")

            if subject and content:
                post.subject = subject
                post.content = content
                post.put()
                self.redirect("/post/%s" % str(post.key().id()))
            else:
                error = "Please input subject and content for a post."
                self.render("Post/edit.html",
                            subject=subject,
                            content=content,
                            user=user,
                            post=post,
                            error=error)
        else:
            return self.redirect("/login?error=Sorry, you have no permission.")


class PostDeletionHandler(Handler):
    """A anonymous user can't process this and the login page will be returned.
    If the user is not the post author,
    the login page and permission error message will be returned.
    """
    def get(self, post_id):
        user = self.get_user_by_cookie()
        key = db.Key.from_path("Post", int(post_id), parent=post_key())
        post = db.get(key)

        if not user:
            self.redirect("/login")

        if user and post and valid_post_author(user, post):
            post.delete()
            self.redirect("/dashboard")
        else:
            return self.redirect("/login?error=Sorry, you have no permission.")
