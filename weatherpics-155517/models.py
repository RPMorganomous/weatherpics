from google.appengine.ext import ndb #get the files that define ndb

class Weatherpics(ndb.Model):
    #Model object used to store image urls in the datastore
    image_url = ndb.StringProperty()
    caption = ndb.StringProperty()
    last_touch_date_time = ndb.DateTimeProperty(auto_now=True)