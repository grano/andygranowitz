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
import webapp2
import jinja2
import logging
import os
import yaml

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

file = open('meta.yaml')
data = yaml.load(file.read())
file.close()

def get_params(PAGE_RE, content_type = "default"):
	p = Content.page_exists(PAGE_RE)
	if content_type == "default":
		content_type = p.content_type
	if p and p.content_type == content_type:
		p = Content.by_permalink(PAGE_RE)
		time_fmt = '%B' + ' ' + '%Y'
		date = p.date.strftime(time_fmt)
		params = dict(permalink = PAGE_RE, content_type = content_type, title = p.title, media_file = p.media_file, 
			media_file_2 = p.media_file_2, media_file_3 = p.media_file_3, media_file_4 = p.media_file_4, media_file_5 = p.media_file_5,
			date = date, post = p.post)
		return params

class MainHandler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class Ashamnu(MainHandler):
    def get(self):
        self.render('posts/' + data['posts'][0]['slug'])

class HomePage(MainHandler):
    def get(self):
    	params = dict(posts = data['posts'], x = 'x')
        self.render('index.html', **params)

class BlogPage(MainHandler):
	def get(self, PAGE_RE):
		logging.error('/posts/' + PAGE_RE)
		self.render('/posts/' + PAGE_RE)

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*\.html)'
app = webapp2.WSGIApplication([
    ('/', HomePage), 
    ('/blog' + PAGE_RE, BlogPage)
], debug=True)
