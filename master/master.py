from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from functools import partial
import json
import requests
import multiprocessing
import logging

secondaries = [{'name': 'secondary-1', 'address': 'http://secondary-1:8081'},
                {'name': 'secondary-2', 'address': 'http://secondary-2:8082'}]
memory_list = list()
id_count = 1
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, level=1)


def send_to_secondary(secondaries, value):
    logging.info('Replication to ' + secondaries['name'] + ' ' + secondaries['address'] + ': '
                 + 'id=' + str(value['id']) + ' msg=' + value['msg'])
    try:
        return secondaries['name'], requests.post(secondaries['address'], json=json.dumps(value)).ok
    except:
        return secondaries['name'], False


def message_handler(val):
    global id_count
    new_value = {'id': id_count, 'msg': val}
    memory_list.append(new_value)
    logging.info('Write in memory: id=' + str(id_count) + ' msg=' + val)
    id_count += 1
    result = True
    pool = multiprocessing.Pool(processes=2)
    for response in pool.map(partial(send_to_secondary, value=new_value), secondaries):
        if not response[1]:
            logging.error('Error with replication to ' + response[0])
            result = False
        else:
            logging.info('Replication to ' + response[0] + ' completed')
    return result

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
        if message_handler(body.decode()):
            self.send_response(200)
        else:
            self.send_response(408)
        self.end_headers()


def main():
    port = 8080
    print('Listening on localhost:%s' % port)
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()