from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import json
import logging

memory_list = list()
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, level=1)


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        if len(memory_list) == 0:
            self.wfile.write("Empty list".encode())
        response = ""
        for row in memory_list:
            response += row['msg'] + '\n'
        self.wfile.write(response.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(json.loads(body))
        try:
            memory_list.append(data)
            logging.info('Saved to ' + self.headers['Host'] + ': '
                         + 'id=' + str(memory_list[-1]['id']) + ' msg=' + memory_list[-1]['msg'])
            self.send_response(200)
        except:
            logging.error('Error on ' + self.headers['Host'] + ': '
                         + 'id=' + str(data['id']) + ' msg=' + data['msg'])
            self.send_response(408)
        self.end_headers()


def main():
    port = 8081
    print('Listening on localhost:%s' % port)
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()