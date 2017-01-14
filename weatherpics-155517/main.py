#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging
import os
import webapp2
import jinja2

from google.appengine.ext import ndb
from models import Weatherpics

# Jinja Environment instance necessary to use Jinja templates.
jinja_env = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  autoescape=True)

PARENT_KEY = ndb.Key("EntityType", "weatherpic_root")

class AddPicAction(webapp2.RequestHandler):
    def post(self):
        logging.info(str(self.request))
        imageurl = self.request.get("imageurl")
        caption = self.request.get("caption")
        new_weatherpic = Weatherpics(parent = PARENT_KEY,
                                    image_url = imageurl,
                                    caption = caption)
        new_weatherpic.put()
        self.redirect(self.request.referrer)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        weatherpic_query = Weatherpics.query(ancestor=PARENT_KEY).order(-Weatherpics.last_touch_date_time)
        template = jinja_env.get_template("templates/weatherpics.html")
        #self.response.write(template.render())
        self.response.write(template.render({"wpq": weatherpic_query}))
        
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/addpic', AddPicAction)
], debug=True)
