from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "localhost"
serverPort = 8010

class server(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
           self.path = '/views/index.html'    
        try:
           open_page = open(self.path[1:]).read()
           self.send_response(200)
        except:
            open_page = "page not found"
            self.send_response(404)

        self.end_headers()
        self.wfile.write(bytes(open_page, 'utf-8'))

if __name__ == "__main__":        
    server = HTTPServer((hostName, serverPort), server)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("Server stopped.")