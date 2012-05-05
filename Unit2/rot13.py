import webapp2
import cgi

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 
			'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
			'v', 'w', 'x', 'y', 'z']

upper_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 
'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
'V', 'W', 'X', 'Y', 'Z']


form="""
<form method="post">
	Enter some text to ROT13"
	<br>
	<textarea type="text area" name=text style="height:100px; width: 400px;">%(value)s
	</textarea>
	<br>
	<input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):

  def write_form(self, value=""):
    self.response.out.write(form % {"value": value} )

  def get(self):
      #self.response.headers['Content-Type'] = 'text/html'
      self.write_form()

  def post(self):
  	  self.write_form(self.escape_html(self.rot13(self.request.get('text'))))

  def escape_html(self, thestring):
  	  return cgi.escape(thestring, quote=True)

  def rot13(self, thestring):

  	i=0
  	newstring =""

  	for character in thestring:
  		if character in alphabet:
  			origcharlocation = alphabet.index(character)
  			newnumber = origcharlocation + 13
  			if newnumber > 25:
  				newnumber = newnumber - 26
  			newstring += alphabet[newnumber]	

  		elif character in upper_alphabet:
  			origcharlocation = upper_alphabet.index(character)	
  			newnumber = origcharlocation + 13
  			if newnumber > 25:
  				newnumber = newnumber -26
  			newstring += upper_alphabet[newnumber]

  		else:
  		  newstring += character  		 
  		i+= 1	  
  	return newstring

app = webapp2.WSGIApplication([('/unit2/rot13', MainPage)], debug=True)