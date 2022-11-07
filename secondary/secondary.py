from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import json
import time

memory_list = list()
#FORMAT = '%(asctime)s %(message)s'
#logging.basicConfig(format=FORMAT, level=1)

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(memory_list).encode())

    def do_POST(self):
        # time.sleep(1)
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        memory_list.append(json.loads(body))
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'Secondary_1 received: ')
        response.write(body)
        self.wfile.write(response.getvalue())

def main():
    port = 8081
    print('Listening on localhost:%s' % port)
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()