import os
import base64
import json
import time
import errno
import shutil
from http.server import BaseHTTPRequestHandler, HTTPServer

#Hantera alla responser vid anrop i ren python
# region
class MyServer(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.script = []  # Initialize script as an instance variable
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if 'v1.0/users' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            with open('./Responses/ID_response.json', 'r') as file:
                self.wfile.write(file.read().encode('utf-8'))
        elif 'TOPDESK_POST/incidents' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            with open('./Responses/Topdesk_incidents_response.json', 'r') as file:
                self.wfile.write(file.read().encode('utf-8'))
        elif '/knowledgeItems?q' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            with open('./Responses/Get_KnowledgeItems/KnowledgeItem_GetByDescription.json', 'r') as file:
                self.wfile.write(file.read().encode('utf-8'))
        elif '/3fa85f64' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            with open('./Responses/Get_KnowledgeItems/KnowledgeItem_GetByID.json', 'r') as file:
                self.wfile.write(file.read().encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Error 404: Not Found')
# endregion
            
# Start HTTP server
#region
server_address = ('', 8000)
httpd = HTTPServer(server_address, MyServer)
print('HTTP server running on port 8000...')
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print('Stopping server...')
    httpd.shutdown()
    httpd.server_close()
    print('Server stopped.')
#endregion