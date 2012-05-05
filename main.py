import webapp2

nav="""
<div>
	<h1>Udacity Projects</h1>
</div>
<div>
Project 1 <a href = "/unit1/helloworld"> Hello World </a>
</div>

<div>
Project 2 <a href ="/unit2/rot13"> Rot 13  </a>
</div>
<div>
Project 3 <a href = "/unit2/signup"> Signup </a>
</div>
"""


class MainPage(webapp2.RequestHandler):
  def write_page(self, value=""):
    self.response.out.write(nav % {"value": value} )

  def get(self):
    #self.response.headers['Content-Type'] = 'text/html'
    self.write_page()


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)