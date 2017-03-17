import os
import webapp2

import jinja2

from google.appengine.ext import db

from base_handler import Handler
from models import Post, User, Comment, Like
from utility import (check_existing_user,
                     make_val_hash,
                     register,
                     SALT,
                     user_key,
                     valid_email,
                     valid_password_format,
                     valid_pw,
                     valid_username,
                     valid_val_hash,)


class RegisterHandler(Handler):
    """Get method displays the register html page.
    Post method verifies and stores data in database if the data is correct.
    """
    def get(self):
        self.render("auth/register.html")

    def post(self):
        has_error = False
        input_username = self.request.get("username")
        input_password = self.request.get("password")
        input_password_confirmation = self.request.get("password_confirmation")
        input_email = self.request.get("email")

        username = valid_username(input_username)
        password = valid_password_format(input_password)
        email = valid_email(input_email)

        params = dict(input_username=input_username,
                      input_email=input_email)

        if not username:
            params["username_error"] = "This is not a valid username."
            has_error = True

        if not password:
            params["password_format_error"] = "This is not a valid password."
            has_error = True
        elif input_password != input_password_confirmation:
            params["password_consistency_error"] = "Passwords don't match"
            has_error = True

        if input_email:
            if not email:
                params["email_error"] = "It must be a valid email address."
                has_error = True

        if check_existing_user(username):
            params["existing_user_error"] = "This user is already exist."
            has_error = True

        if has_error:
            self.render("auth/register.html", **params)
        else:
            username_key = register(username, password, email)
            username_id = username_key.id()
            cookie_hash = make_val_hash(username_id, SALT)
            self.response.headers.add_header("Set-Cookie",
                                             "user_id=%s" % cookie_hash)
            self.redirect("/dashboard")


class LoginHandler(Handler):
    def get(self):
        """get method will display login html page"""
        user = self.get_user_by_cookie()
        permission_error = self.request.get("error")
        self.render("auth/login.html",
                    user=user,
                    permission_error=permission_error)

    def post(self):
        """post method will varify then accept user's cridentials,
        if the cridentials are correct.
        The cookie will be stored in the broswer as well.
        When decrypting the cookie, the system will know who has logged.
        """
        input_username = str(self.request.get("username"))
        input_password = str(self.request.get('password'))
        valid_credential = False
        error = "Invalid Credentials"
        # This query looks like the following mysql query.
        # "select * from User where username = input_username limit 1"
        # get() will get the first result. Using fetch() will get all results.
        user = User.all().filter("username = ", input_username).get()

        if user:
            valid_pw_result = valid_pw(input_username,
                                       input_password,
                                       user.password)
            if input_username == user.username and valid_pw_result:
                username_id = user.key().id()
                cookie_hash = make_val_hash(username_id, SALT)
                self.response.headers.add_header("Set-Cookie",
                                                 "user_id=%s" % cookie_hash)
                valid_credential = True
                error = ""

            if valid_credential:
                self.redirect("/dashboard")

        self.render("auth/login.html",
                    input_username=input_username,
                    error=error)


class DashboardHandler(Handler):
    """This will display dashboard html page."""
    def get(self):
        user = self.get_user_by_cookie()
        if user:
            self.render("dashboard.html", user=user)
        else:
            self.redirect("/login")


class LogoutHandler(Handler):
    """ The cookie will be set to blank when the user is loging out."""
    def get(self):
        self.response.headers.add_header("Set-Cookie", "user_id=; Path=/")
        self.redirect("/")


class ResetPasswordHandler(Handler):
    """When a registed user resets password, this will display reset html page.
    When the anonymous user resets password, login page will be returned.
    Reset password function is just for fun,
    cause when registering a new account,
    the email address is optional, there is no way to reset password without
    sending reset password link to user's email.
    """
    def get(self):
        user = self.get_user_by_cookie()
        if user:
            self.redirect("/post")
        else:
            self.render("auth/passwords/reset.html")


class RefreshHandler(Handler):
    """When visiting this url, the whole database will be cleared."""
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post")
        users = db.GqlQuery("SELECT * FROM User")
        comments = db.GqlQuery("SELECT * FROM Comment")
        likes = db.GqlQuery("SELECT * FROM Like")

        if posts:
            db.delete(posts)

        if users:
            db.delete(users)

        if comments:
            db.delete(comments)

        if likes:
            db.delete(likes)
