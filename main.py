#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import GBEntry

guestbook_dir = os.path.join(os.path.dirname(__file__), "guestbook")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(guestbook_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        entries = GBEntry.query().fetch()
        params = {"entries": entries}
        return self.render_template("guestbook.html", params=params)

    def post(self):
        getname = self.request.get("name")
        getemail = self.request.get("email")
        gettext = self.request.get("text")

        if not getname:
            getname = "Anonymous"

        entry = GBEntry(name=getname, email=getemail, text=gettext)
        entry.put()

        entries = GBEntry.query().fetch()
        params = {"entries": entries}
        return self.render_template("guestbook.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler)
], debug=True)