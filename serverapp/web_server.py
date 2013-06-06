#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.


import string,cgi,time,subprocess
import urlparse
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#import pri

class MyHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		print '>>> request ' + self.path
		o = urlparse.urlparse(self.path)
		par = urlparse.parse_qs(o.query)
		simpleurl = urlparse.urlsplit(self.path)
		print simpleurl.path
		try:
			if simpleurl.path.endswith(".html"):
				f = open(curdir + sep + ".." + sep + "webapp" + sep + simpleurl.path) #self.path has /test.html
				#note that this potentially makes every file on your computer readable by the internet

				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				self.wfile.write(f.read())
				
				f.close()
				return

			if self.path.endswith(".jpg") or self.path.endswith(".jpeg"):
				f = open(curdir + sep + ".." + sep + "webapp" + sep + "imgs" + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',	'image/jpeg')
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
				return
			if self.path.endswith(".py") or self.path.endswith(".pyc"):
				proc = subprocess.Popen(['python', curdir + sep + self.path,  'arg1 arg2 arg3 arg4'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write(proc.communicate()[0])
				return
			if self.path.endswith(".esp"):   #our dynamic content
				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				self.wfile.write("hey, today is the" + str(time.localtime()[7]))
				self.wfile.write(" day in the year " + str(time.localtime()[0]))
				return
				
			if self.path.endswith(".ico"):
				return

			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)


	def do_POST(self):
		global rootnode
		try:
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				query=cgi.parse_multipart(self.rfile, pdict)
				self.send_response(301)

				self.end_headers()
				upfilecontent = query.get('upfile')
				#print "filecontent", upfilecontent[0]
				self.wfile.write("<HTML>POST OK.<BR><BR>")
				#self.wfile.write(upfilecontent[0]);
				f = open('workfile', 'w')
				f.write(upfilecontent[0])
				#print upfilecontent[1]

		except :
			pass

def main():
	try:
		server = HTTPServer(('', 80), MyHandler)
		print 'started httpserver...'
		server.serve_forever()
	except KeyboardInterrupt:
		print '^C received, shutting down server'
		server.socket.close()

if __name__ == '__main__':
	main()
