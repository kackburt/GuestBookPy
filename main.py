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
        entries = GBEntry.query(GBEntry.visible == True).fetch()
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


class EditEntryHandler(BaseHandler):
    def get(self, dbobject_id):
        entry = GBEntry.get_by_id(int(dbobject_id))
        params = {"entry": entry}
        return self.render_template("guestbook_edit.html", params=params)

    def post(self, dbobject_id):
        getnewname = self.request.get("newname")
        getnewtext = self.request.get("newtext")
        entry = GBEntry.get_by_id(int(dbobject_id))
        entry.name = getnewname
        entry.text = getnewtext
        entry.put()
        return self.redirect_to("guestbook-home")


class DeleteEntryHandler(BaseHandler):
    def get(self, dbobject_id):
        entry = GBEntry.get_by_id(int(dbobject_id))
        params = {"entry": entry}
        return self.render_template("guestbook_delete.html", params=params)

    def post(self, dbobject_id):
        entry = GBEntry.get_by_id(int(dbobject_id))
        entry.key.delete()
        return self.redirect_to("guestbook-home")


class VisibilityEntryHandler(BaseHandler):
    def get(self, dbobject_id):
        entry = GBEntry.get_by_id(int(dbobject_id))
        params = {"entry": entry}
        return self.render_template("guestbook_visibility.html", params=params)

    def post(self, dbobject_id):
        entry = GBEntry.get_by_id(int(dbobject_id))
        entry.visible = False
        entry.put()
        return self.redirect_to("guestbook-home")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="guestbook-home"),
    webapp2.Route('/edit/<dbobject_id:\d+>', EditEntryHandler),
    webapp2.Route('/delete/<dbobject_id:\d+>', DeleteEntryHandler),
    webapp2.Route('/invisible/<dbobject_id:\d+>', VisibilityEntryHandler)
], debug=True)