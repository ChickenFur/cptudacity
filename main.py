import webapp2

nav="""
<div>
	<h1>Udacity Projects</h1>
</div>
<div>
Project 1 <a href = "/unit1/helloworld"> Hello World </a>
</div>

<div>
Project 2 rot13 <a href ="/unit2/rot13"> Rot 13  </a>
</div>
<div>
Project 2 Signup <a href = "/unit2/signup"> Signup </a>
</div>
<div>
Project 3 Blog	<a href = "/unit3/blog"> Blog </a>
</div>

"""


class MainPage(webapp2.RequestHandler):
  def write_page(self, value=""):
    self.response.out.write(nav % {"value": value} )

  def get(self):
    #self.response.headers['Content-Type'] = 'text/html'
    self.write_page()


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)