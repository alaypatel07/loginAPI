__author__ = 'alay'

import traceback
from tornado.web import RequestHandler
from src import handledoc
from src import handler
from src.handletoken import HandleToken


class LogoutHandler(handler.LoginRequestHandler):
    def post(self, *args, **kwargs):
        token = self.get_argument('token')
        token_handler = HandleToken(token)
        if token_handler.exists():
            if token_handler.del_token():
                del token_handler
                self.send_error(200)
        else:
            self.message = "tokenExpired"
            self.send_error(404)