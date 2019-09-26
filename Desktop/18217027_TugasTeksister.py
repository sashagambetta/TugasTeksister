import http.server
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
import base64

username = "ujicoba"
password = "ujicoba"
auth_keyword = username + ":" + password
auth_keyword_b64 = "Basic " + str(base64.b64encode(auth_keyword.encode("utf-8")),"utf-8")

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_HEAD(self):
        print("send header")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_AUTHHEAD(self):
        print("send header")
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        #global auth_key
        '''Present frontpage with user authentication.'''
        if self.headers.get('authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write(b'no auth header received')
            pass
        elif self.headers.get('authorization') == auth_keyword_b64:
            return SimpleHTTPRequestHandler.do_GET(self)
            pass
        else:
            self.do_AUTHHEAD()
            #print(self.headers.get('authorization'))
            self.wfile.write(b'not authenticaticated')
            pass
    
port = 4444
with HTTPServer(("",port), RequestHandler) as httpd:
    print("serving at port ",port)
    httpd.socket = ssl.wrap_socket(httpd.socket, keyfile = "key.pem", certfile = "certificate.pem", server_side=True)
    httpd.serve_forever()
