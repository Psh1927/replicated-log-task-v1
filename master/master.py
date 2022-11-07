from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from functools import partial
import json
import requests
import multiprocessing
import logging

secondaries = [{'name': 'secondary-1', 'address': 'http://secondary-1:8081'},
               {'name': 'secondary-2', 'address': 'http://secondary-2:8081'}]
memory_list = list()
id_count = 1
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, level=1)


def send_to_secondary(secondaries, value):
    logging.info('Replication to ' + secondaries['name'] + ' ' + secondaries['address'] + ': '
                 + 'id=' + str(value['id']) + ' msg=' + value['msg'])
    return requests.post(secondaries['address'], json=value).ok


def message_handler(val):
    global id_count
    new_value = {'id': id_count, 'msg': val}
    memory_list.append(new_value)
    logging.info('Write in memory: id=' + str(id_count) + ' msg=' + val)
    id_count += 1
    pool = multiprocessing.Pool(processes=2)
    pool.map(partial(send_to_secondary, value=new_value), secondaries)


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(memory_list).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'Received: ')
        response.write(body)
        message_handler(body.decode())
        self.wfile.write(response.getvalue())

def main():
    port = 8080
    print('Listening on localhost:%s' % port)
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()