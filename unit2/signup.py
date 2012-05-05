import webapp2
import cgi
import re
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$") 
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

form="""
<form method="post">
	<b>Signup</b>
<div>
  <label>UserName 
	<input type="textbox" name="username" value=%(username)s></text> <text style="color:red;">  %(username_error)s </text>
  </label>
</div>
<div>
  <label>Password
  <input type="password" name="password" ></text> <text style="color:red;"> %(password_error)s  </text>
  </label>
</div>
<div>
  <label>Verify
  <input type="password" name="verify" ></text> <text style="color:red;">%(verify_error)s  </text>
  </label>
</div>
<div>
  <label>email
  <input type="textbox" name="email" value=%(email)s></text>  <text style="color:red;">  %(email_error)s  </text>
  </label>
</div>
	<input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):

  def write_form(self, username="", email="", username_error="",password_error="",verify_error="",email_error=""):

    self.response.out.write(form % {"username": username, 
                                    "email": email ,
                                    "username_error":username_error, 
                                    "password_error": password_error,
                                    "verify_error": verify_error,
                                    "email_error": email_error} )

  def get(self):
      #self.response.headers['Content-Type'] = 'text/html'
      self.write_form()

  def post(self):

     
      #if everything validates:    
      if ( self.validate_username(self.request.get("username")) 
          and self.validate_password(self.request.get("password"))
          and self.validate_verify_password(self.request.get("verify")) 
          and self.validate_email(self.request.get("email"))):

        redirectstring = "/welcome?username=" + self.request.get("username")
        self.redirect(redirectstring)

      else:
        username_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""

        if (not self.validate_username(self.request.get("username"))):
          username_error = "That's not a valid UserName"

        if (not self.validate_password(self.request.get("password"))):
          password_error = "That's not a valid password"

        if (not self.validate_verify_password(self.request.get("verify"))):
          verify_error = "Passwords do not match"

        if (not self.validate_email(self.request.get('email'))):
          email_error = "That's not a valid email"

        self.write_form(username = self.escape_html(self.request.get('username')),
                        username_error=username_error,
                        password_error=password_error,
                        verify_error=verify_error,
                        email_error=email_error,
                        email = self.escape_html(self.request.get('email'))
                        )

  def escape_html(self, thestring):
  	  return cgi.escape(thestring, quote=True)

  def validate_username(self, username):  
  	return USER_RE.match(username)

  def validate_password(self, password):
    return PASSWORD_RE.match(password)

  def validate_verify_password(self, verify):
    return verify == self.request.get("password")

  def validate_email(self, email):
    return EMAIL_RE.match(email)

class WelcomePage(webapp2.RequestHandler):
  def get(self):
    string = "Welcome, " + self.request.get("username")
    self.response.out.write(string)


app = webapp2.WSGIApplication([('/unit2/signup', MainPage), ('/unit2/signup/welcome', WelcomePage)], debug=True)