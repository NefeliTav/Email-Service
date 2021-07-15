import os
from http.server import HTTPServer, CGIHTTPRequestHandler
from subprocess import Popen

os.chdir('.')

# Create server object listening the port 80
server_object = HTTPServer(server_address=('0.0.0.0', 8080), RequestHandlerClass=CGIHTTPRequestHandler)

remote_host = 'http://localhost:80'
cmd = f'while true; do date >> index.html; curl {remote_host} >> index.html 2>&1; sleep 3; done'
processes = Popen(cmd, shell=True)

server_object.serve_forever()