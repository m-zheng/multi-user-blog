import os
import webapp2
import jinja2

from google.appengine.ext import db

from utility import valid_val_hash, SALT, user_key


template_dir = os.path.join(os.path.dirname(__file__), "../resources/views")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Handler(webapp2.RequestHandler):
    """This is web request handler, it uses webapp2 and jinja2 lib."""
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def get_user_by_cookie(self):
        """This method fetches and decrypts cookie.
        It also checks whether the use is logged in or not.
        """
        cookie_hash = self.request.cookies.get("user_id")
        if cookie_hash and valid_val_hash(cookie_hash, SALT):
            username_id = cookie_hash.split("|")[0]
            key = db.Key.from_path("User",
                                   int(username_id),
                                   parent=user_key())
            user = db.get(key)
            return user
