#!/usr/bin/python
import BaseHTTPServer

from router import Router


class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.router = Router()
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request,
                                                       client_address,
                                                       server)

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        response = self.router.dispatch(self.path, self)
        self.end_headers()
        self.wfile.write(response)
