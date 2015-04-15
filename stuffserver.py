from http.server import BaseHTTPRequestHandler,HTTPServer
import time
import sys

hostname = "localhost"
portnumber = 8000

REDIRECTIONS = {"/findit/": "localhost:8000/findit.html/"}
LAST_RESORT = "http://craigslist.org/"

class RedirectHandler(BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(301)
        s.send_header('Content-type', 'text/html')
        S.end_headers()
    def do_GET(s):
        s.do_HEAD()

def launch_server():
    #server_class = BaseHTTPServer.HTTPServer
    httpd = HTTPServer((hostname, portnumber), RedirectHandler)
    print(time.asctime(), "Server starts - %s:%s" % (hostname, portnumber))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (hostname, portnumber))
