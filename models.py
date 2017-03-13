from google.appengine.ext import ndb

class GBEntry(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    text = ndb.TextProperty()
    visible = ndb.BooleanProperty(default=True)
    created = ndb.DateTimeProperty(auto_now_add=True)