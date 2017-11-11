#!/usr/bin/env python
import os
import jinja2
import webapp2
import random

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))

class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

class LottoHandler(BaseHandler):
    def get(self):
        winning_numbers = generator(8)

        params = {"winning_numbers": winning_numbers}

        return self.render_template("lotto.html", params=params)

def generator(amount):
    list_numbers = []

    while True:
        if len(list_numbers) == amount:
            break

        winning_num = random.randint(1,39)

        if winning_num not in list_numbers:
            list_numbers.append(winning_num)

    return sorted(list_numbers)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/lotto', LottoHandler),
], debug=True)
