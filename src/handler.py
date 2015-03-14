__author__ = 'alay'

from tornado.web import RequestHandler
from os.path import dirname
import traceback
import json


class LoginRequestHandler(RequestHandler):
    def initialize(self):
        self.root = dirname(__file__).rstrip('/src')
        self.message = ''

    def write_error(self, status_code, **kwargs):
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'application/json')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            if self.message == '':
                self.message = self._reason
            message = dict()
            message['status'] = str(status_code)
            message['reason'] =  self.message
            self.set_header('Content-Type', 'application/json')
            self.finish(json.dumps(message))