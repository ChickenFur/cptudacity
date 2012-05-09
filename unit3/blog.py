import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
							   autoescape=True)

class Handler(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  def render (self, template, **kw):
    self.write(self.render_str(template, **kw))	

def blog_key(name = 'default'):
  return db.Key.from_path('MyBlogs', name)


class BlogPost(db.Model):
  title = db.StringProperty(required = True)
  blogtext = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)
  last_modified = db.DateTimeProperty(auto_now_add = True)
  

class MainPage(Handler):
  def get(self):
    posts= db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC limit 10")

    self.render("front.html", posts=posts)

class DisplayIndividualBlogPost(Handler):
  def get(self, post_id):
    key = db.Key.from_path('BlogPost', int(post_id), parent=blog_key())

    #post = BlogPost.get_by_id(int(post_id))

    post = db.get(key)

    if not post:
      self.write("Something is Wrong.  The blog Must be missing")
      self.write(post)
      return

    self.render("post.html", post = post)

class CreateBlogPost(Handler):
  def render_front(self, title="", blogtext="", error=""):
    self.render("newpost.html", title=title, blogtext=blogtext, error=error)

  def get(self):
    self.render_front()

  def post(self):
    title = self.request.get("subject")
    blogtext = self.request.get("content")

    if title and blogtext:
      b = BlogPost(parent = blog_key(), title = title, blogtext = blogtext)
      b.put()

      self.redirect("/unit3/blog/%s" % str(b.key().id()))

    else:
      error = "We need both a title and  blogtext"
      self.render_front(title = title, blogtext = blogtext, error = error)


app = webapp2.WSGIApplication([ ('/unit3/blog', MainPage), 
                                ('/unit3/blog/([0-9]+)', DisplayIndividualBlogPost),
                                ('/unit3/blog/newpost', CreateBlogPost)], debug=True)

