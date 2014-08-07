#!/usr/bin/env python

# Handler for GitHub webhook.
# By Pengyu CHEN (pengyu[at]libstarrify.so)
# COPYLEFT, ALL WRONGS RESERVED.

try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os


class Server(BaseHTTPRequestHandler):
    def do_POST(self):
        secret = 'YangJiCooperAHAHAHA'
        if self.path == '/%s' % secret:
            os.system('git pull')


def main():
    httpd = HTTPServer(('', 8192), Server)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
